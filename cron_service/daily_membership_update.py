import asyncio
import datetime
import aiohttp

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_upsert

from helpers.neon_creds import N_HEADERS, N_BASE_URL
from helpers.get_neon_data import (
    get_all_accounts,
    get_acct_membership_data,
)

from engine import engine
from schema import MembershipCount


async def get_active_members_count(session: aiohttp.ClientSession) -> int:

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
    ]

    output_fields = ["Account ID"]

    count = 0

    async for page in get_all_accounts(session, search_params, output_fields):
        if page["pagination"]["currentPage"] < page["pagination"]["totalPages"]:
            print(
                f"Page {page['pagination']['currentPage'] + 1}",
                "of",
                page["pagination"]["totalPages"],
            )
            accts = page["searchResults"]
        else:
            break

        count += len(accts)

    return count


async def get_acct_signups_count(session: aiohttp.ClientSession) -> int:

    search_params = [
        {
            "field": "Account Type",
            "operator": "EQUAL",
            "value": "Individual",
        },
        {
            "field": "Account Created Date",
            "operator": "EQUAL",
            "value": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
        },
    ]

    output_fields = ["Account ID"]

    count = 0

    async for page in get_all_accounts(session, search_params, output_fields):
        if page["pagination"]["currentPage"] < page["pagination"]["totalPages"]:
            accts = page["searchResults"]
        else:
            break

        count += len(accts)

    return count


async def get_churns_and_signups_count(
    session: aiohttp.ClientSession,
) -> tuple[int, int]:

    base = [
        {
            "field": "Account Type",
            "operator": "EQUAL",
            "value": "Individual",
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
    ]

    churns = base.copy()

    churns.append(
        {
            "field": "Membership Expiration Date",
            "operator": "EQUAL",
            "value": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
        }
    )

    joins = base.copy()

    joins.append(
        {
            "field": "Membership Start Date",
            "operator": "EQUAL",
            "value": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
        }
    )

    churn_count = 0
    member_signups_count = 0

    async for page in get_all_accounts(session, churns, ["Account ID"]):
        if page["pagination"]["currentPage"] < page["pagination"]["totalPages"]:
            accts = page["searchResults"]
        else:
            break

        churn_count += len(accts)

    async for page in get_all_accounts(session, joins, ["Account ID"]):
        if page["pagination"]["currentPage"] < page["pagination"]["totalPages"]:
            accts = page["searchResults"]
        else:
            break

        for acct in accts:
            memberships = await get_acct_membership_data(session, acct["Account ID"])

            if len(memberships) == 1:
                member_signups_count += 1
                continue

            if memberships[-1].start_date - memberships[
                -2
            ].end_date > datetime.timedelta(days=1):
                member_signups_count += 1

    return (churn_count, member_signups_count)


async def get_daily_count() -> dict[str, int]:
    async with aiohttp.ClientSession(headers=N_HEADERS, base_url=N_BASE_URL) as session:

        async with asyncio.TaskGroup() as tg:
            active_members_count = tg.create_task(get_active_members_count(session))
            acct_signups_count = tg.create_task(get_acct_signups_count(session))

            churns_and_signups = tg.create_task(get_churns_and_signups_count(session))

    churns_and_signups = churns_and_signups.result()

    new_counts = {
        "total_active_count": active_members_count.result(),
        "churn_count": churns_and_signups[0],
        "member_signups_count": churns_and_signups[1],
        "acct_signups_count": acct_signups_count.result(),
    }

    return new_counts


def update_membership_table(
    sql_engine: sqlalchemy.Engine,
    new_counts: dict[str, int],
) -> None:
    """Update the database with today's member counts"""

    with Session(sql_engine) as session:

        new_counts["date"] = datetime.date.today() - datetime.timedelta(days=1)

        stmt = pg_upsert(MembershipCount).values(new_counts)

        stmt = stmt.on_conflict_do_update(
            index_elements=[MembershipCount.date],
            set_={
                MembershipCount.total_active_count: stmt.excluded.total_active_count,
                MembershipCount.churn_count: stmt.excluded.churn_count,
                MembershipCount.member_signups_count: stmt.excluded.member_signups_count,
                MembershipCount.acct_signups_count: stmt.excluded.acct_signups_count,
            },
        )

        session.execute(stmt)

        session.commit()


def main() -> None:
    daily_count = asyncio.run(get_daily_count())

    update_membership_table(engine, daily_count)


if __name__ == "__main__":
    main()
