import re
import asyncio
import logging
import datetime
import aiohttp

from sqlalchemy import update, select
from sqlalchemy.orm import Session

from helpers.neon_creds import N_HEADERS, N_BASE_URL
from helpers.get_neon_data import (
    get_all_accounts,
)

from engine import engine
from schema import Member


def update_member_zips_in_db(bulk_updates: list[dict[str, int]]) -> None:

    with Session(engine) as sql_session:
        sql_session.execute(update(Member), bulk_updates)
        sql_session.commit()


def get_all_neon_ids_in_db() -> list[int]:
    ids = []

    with Session(engine) as session:
        stmt = select(Member)
        for row in session.execute(stmt):
            ids.append(row.Member.neon_id)

    return ids


async def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Beginning zip code updates on %s", datetime.date.today())

    pattern = re.compile(r"^(\d+)(?:-|$)")

    all_neon_ids = get_all_neon_ids_in_db()

    search_params = [
        {
            "field": "Account Type",
            "operator": "EQUAL",
            "value": "Individual",
        },
        {"field": "Account ID", "operator": "IN_RANGE", "valueList": all_neon_ids},
    ]

    output_fields = ["Account ID", "Zip Code"]

    bulk_updates = []

    async with aiohttp.ClientSession(headers=N_HEADERS, base_url=N_BASE_URL) as session:

        count = 0
        async for page in get_all_accounts(session, search_params, output_fields):
            if page["pagination"]["currentPage"] < page["pagination"]["totalPages"]:
                accts = page["searchResults"]
            else:
                break

            for i in accts:
                if not i["Zip Code"]:
                    continue

                zip_code = None

                zip_code = pattern.match(i["Zip Code"])

                if zip_code:
                    zip_code = int(zip_code.group(1))

                bulk_updates.append(
                    {"neon_id": int(i["Account ID"]), "zip_code": zip_code}
                )

                count += 1

                if count % 50 == 0:
                    print(f"--- {count} ---")

    update_member_zips_in_db(bulk_updates=bulk_updates)


if __name__ == "__main__":
    asyncio.run(main())
