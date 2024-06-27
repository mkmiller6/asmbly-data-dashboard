# pylint: disable=import-error

import asyncio
import datetime
import logging
import os
import re
import aiohttp
import requests
import googlemaps
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_upsert

from sklearn.pipeline import Pipeline
from sksurv.ensemble import GradientBoostingSurvivalAnalysis

from helpers.neon_creds import N_HEADERS, N_BASE_URL, is_docker
from helpers.get_neon_data import (
    get_all_accounts,
    get_individual_account,
)
from helpers.enums import Attended, AccountCurrentMembershipStatus
from helpers.neon_dataclasses import NeonAccount
from helpers.default_dataframe import default_params
from helpers.survival_model import transform_pipeline, survival_model

from engine import engine
from schema import Member

if not is_docker():
    from dotenv import load_dotenv

    load_dotenv()

GOOGLE_MAPS_API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]


def find_member_risk(
    df: pd.DataFrame, pipeline: Pipeline, model: GradientBoostingSurvivalAnalysis
) -> float:
    X = df.drop(columns=["membership_cancelled", "duration"])

    X_transformed = pipeline.transform(X)
    risk = model.predict(X_transformed)

    return risk[0]


def update_member_df(
    df: pd.DataFrame, acct: NeonAccount, gmaps: googlemaps.Client, asmbly_geocode: str
) -> pd.DataFrame:
    attended = acct.event_info.has_taken_classes()
    distances = acct.location_info.get_distance_from_asmbly(gmaps, asmbly_geocode)

    df["neon_id"] = acct.basic_info.neon_id
    df["email"] = acct.basic_info.email
    df["first_name"] = acct.basic_info.first_name
    df["last_name"] = acct.basic_info.last_name
    df["has_op_id"] = acct.basic_info.openpath_id is not None
    df["has_discourse_id"] = acct.basic_info.discourse_id is not None
    df["age"] = acct.basic_info.age
    df["gender"] = acct.basic_info.gender
    df["referral_source"] = acct.basic_info.referral_source
    df["family_membership"] = acct.membership_info.family_membership
    df["waiver_signed"] = acct.basic_info.waiver_date is not None
    df["orientation_attended"] = acct.basic_info.orientation_date is not None
    df["taken_MSS"] = attended[Attended.MSS]
    df["taken_WSS"] = attended[Attended.WSS]
    df["taken_cnc_class"] = attended[Attended.CNC]
    df["taken_lasers_class"] = attended[Attended.LASERS]
    df["taken_3dp_class"] = attended[Attended.PRINTING_3D]
    df["teacher"] = acct.basic_info.teacher
    df["steward"] = acct.basic_info.steward
    df["num_classes_before_joining"] = acct.get_classes_before_first_membership()
    df["num_classes_attended"] = acct.event_info.total_classes_attended
    df["total_dollars_spent"] = acct.total_dollars_spent()
    df["time_from_asmbly"] = distances["time"]

    cancelled = (
        acct.membership_info.current_membership_status
        == AccountCurrentMembershipStatus.INACTIVE
    )

    df["membership_cancelled"] = cancelled
    df["annual_membership"] = acct.membership_info.has_annual_membership
    df["duration"] = acct.membership_info.membership_duration

    return df


def update_member_in_db(acct: NeonAccount, df: pd.DataFrame) -> None:

    churn_risk = find_member_risk(df, transform_pipeline, survival_model)

    pattern = re.compile(r"^(\d+)(?:-|$)")

    zip_code = None

    if acct.location_info.zip:
        zip_code = pattern.match(acct.location_info.zip)

    if zip_code:
        zip_code = int(zip_code.group(1))

    with Session(engine) as sql_session:
        stmt = pg_upsert(Member).values(
            zip_code=zip_code,
            membership_duration=acct.membership_info.membership_duration,
            risk_score=churn_risk,
            neon_id=int(acct.basic_info.neon_id),
            first_name=acct.basic_info.first_name,
            last_name=acct.basic_info.last_name,
            email=acct.basic_info.email,
            active=acct.membership_info.current_membership_status
            == AccountCurrentMembershipStatus.ACTIVE,
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[Member.neon_id],
            set_={
                Member.zip_code: stmt.excluded.zip_code,
                Member.membership_duration: stmt.excluded.membership_duration,
                Member.risk_score: stmt.excluded.risk_score,
                Member.active: stmt.excluded.active,
                Member.first_name: stmt.excluded.first_name,
                Member.last_name: stmt.excluded.last_name,
                Member.email: stmt.excluded.email,
            },
        )
        sql_session.execute(stmt)
        sql_session.commit()


async def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Beginning daily member risk updates for %s", datetime.date.today())

    requests_session = requests.Session()
    gmaps = googlemaps.Client(
        key=GOOGLE_MAPS_API_KEY, requests_session=requests_session
    )
    asmbly_geocode = gmaps.geocode("9701 Dessau Rd Ste 304, Austin, TX 78754")[0][
        "geometry"
    ]["location"]

    search_params = [
        {
            "field": "Account Type",
            "operator": "EQUAL",
            "value": "Individual",
        },
        {
            "field": "Account Current Membership Status",
            "operator": "EQUAL",
            "value": "Active",
        },
        {
            "field": "Membership Level",
            "operator": "EQUAL",
            "value": "Regular Membership",
        },
        {
            "field": "Membership Transaction Status",
            "operator": "EQUAL",
            "value": "Succeeded",
        },
        {
            "field": "Membership Cost",
            "operator": "GREATER_THAN",
            "value": 0,
        },
        {
            "field": "Most Recent Membership Only",
            "operator": "EQUAL",
            "value": "Yes",
        },
        {
            "field": "First Membership Enrollment Date",
            "operator": "LESS_THAN",
            "value": (datetime.date.today() - datetime.timedelta(days=14)).isoformat(),
        },
    ]

    output_fields = ["Account ID", "Account Current Membership Status"]

    async with aiohttp.ClientSession(headers=N_HEADERS, base_url=N_BASE_URL) as session:

        count = 0
        async for page in get_all_accounts(session, search_params, output_fields):
            if page["pagination"]["currentPage"] < page["pagination"]["totalPages"]:
                accts = page["searchResults"]
            else:
                break

            for i in accts:
                member_df = default_params.copy(deep=True)

                acct = await get_individual_account(
                    session, i["Account ID"], i["Account Current Membership Status"]
                )

                member_df = update_member_df(member_df, acct, gmaps, asmbly_geocode)

                update_member_in_db(acct, member_df)

                count += 1

                if count % 50 == 0:
                    print(f"--- {count} ---")


if __name__ == "__main__":
    asyncio.run(main())
