"""Seed the database with the intitial membership counts data"""

import datetime
import polars as pl

from engine import connection_uri


def load_subscriber_data(file_path: str) -> pl.LazyFrame:
    """Load data from CSV file"""
    return (
        pl.scan_csv(file_path)
        .select(
            (pl.col("Date").str.to_date("%m/%d/%Y") - datetime.timedelta(days=1)).alias(
                "date"
            ),
            pl.col("Subscriber Count").cast(pl.Int32).alias("total_active_count"),
        )
        .sort(by="date")
    )


def load_account_creations(file_path: str) -> pl.LazyFrame:
    """Load data from CSV file"""
    return (
        pl.scan_csv(file_path)
        .select(
            pl.col("Account ID").alias("acct_signups_count"),
            pl.col("Account Created Date/Time")
            .str.to_datetime("%m/%d/%Y %I:%M %p")
            .cast(pl.Date)
            .alias("created_on_date"),
        )
        .group_by("created_on_date")
        .agg(pl.col("acct_signups_count").count())
        .sort(by="created_on_date")
    )


def find_churn_dates(struct: list[dict[str, datetime.date]]) -> list[datetime.date]:
    """Find the churn dates"""
    mem_start_dates = [s["start_date"] for s in struct]
    mem_end_dates = [s["expired_on_date"] for s in struct]

    churn_dates = []

    for i in range(len(mem_start_dates) - 1):
        if mem_start_dates[i + 1] - mem_end_dates[i] > datetime.timedelta(days=1):
            churn_dates.append(mem_end_dates[i])

    if mem_end_dates[-1] < datetime.date.today():
        churn_dates.append(mem_end_dates[-1])

    return churn_dates


def load_churns(file_path: str) -> pl.LazyFrame:
    """Load data from CSV file"""
    return (
        pl.scan_csv(file_path)
        .select(
            pl.col("Account ID").alias("neon_id"),
            pl.col("Membership Start Date").str.to_date("%m/%d/%Y").alias("start_date"),
            pl.col("Membership Expiration Date")
            .str.to_date("%m/%d/%Y")
            .alias("expired_on_date"),
        )
        .sort(by="expired_on_date")
        .group_by("neon_id")
        .agg(
            pl.struct(["start_date", "expired_on_date"])
            .map_elements(
                lambda s: find_churn_dates(s),  # pylint: disable=unnecessary-lambda
                return_dtype=pl.List(pl.Date),
            )
            .alias("churn_dates")
        )
        .explode("churn_dates")
        # .filter(pl.col("neon_id") == 3944)
        .filter(pl.col("churn_dates").is_not_null())
        .group_by("churn_dates")
        .agg(pl.col("neon_id").count().alias("churn_count"))
    )


def find_join_dates(struct: list[dict[str, datetime.date]]) -> list[datetime.date]:
    """Find the join/rejoin dates"""
    mem_start_dates = [s["start_date"] for s in struct]
    mem_end_dates = [s["expired_on_date"] for s in struct]

    join_dates = []

    join_dates.append(mem_start_dates[0])

    for i in range(len(mem_start_dates) - 1):
        if mem_start_dates[i + 1] - mem_end_dates[i] > datetime.timedelta(days=1):
            join_dates.append(mem_start_dates[i + 1])

    return join_dates


def load_joins(file_path: str) -> pl.LazyFrame:
    """Load data from CSV file"""
    return (
        pl.scan_csv(file_path)
        .select(
            pl.col("Account ID").alias("neon_id"),
            pl.col("Membership Start Date").str.to_date("%m/%d/%Y").alias("start_date"),
            pl.col("Membership Expiration Date")
            .str.to_date("%m/%d/%Y")
            .alias("expired_on_date"),
        )
        .sort(by="start_date")
        .group_by("neon_id")
        .agg(
            pl.struct(["start_date", "expired_on_date"])
            .map_elements(
                lambda s: find_join_dates(s),  # pylint: disable=unnecessary-lambda
                return_dtype=pl.List(pl.Date),
            )
            .alias("join_dates")
        )
        .explode("join_dates")
        # .filter(pl.col("neon_id") == 3944)
        .filter(pl.col("join_dates").is_not_null())
        .group_by("join_dates")
        .agg(pl.col("neon_id").count().alias("member_signups_count"))
    )


def join_dataframes(
    subscriber_data: pl.LazyFrame,
    account_creations: pl.LazyFrame,
    churns: pl.LazyFrame,
    joins: pl.LazyFrame,
) -> pl.DataFrame:
    """Concatenate dataframes to create a single dataframe"""

    return (
        subscriber_data.join(
            account_creations,
            how="outer_coalesce",
            left_on="date",
            right_on="created_on_date",
        )
        .join(churns, how="outer_coalesce", left_on="date", right_on="churn_dates")
        .join(joins, how="outer_coalesce", left_on="date", right_on="join_dates")
        .fill_null(0)
        .sort(by="date", descending=True)
        # .with_columns(
        #     (pl.col("joins") - pl.col("churns")).cum_sum(reverse=True).alias("cum"),
        # )
        .collect()
    )


def write_db_from_csv(table_name: str, db_uri: str) -> None:
    """Seed the database with the intitial member data"""
    sub_data = load_subscriber_data("./data/subscriber_counts.csv")

    account_creations = load_account_creations("./data/account_creations.csv")

    churns = load_churns("./data/all_memberships.csv")

    joins = load_joins("./data/all_memberships.csv")

    data = join_dataframes(sub_data, account_creations, churns, joins)

    data.write_database(
        table_name=table_name, connection=db_uri, if_table_exists="append"
    )

    # print(data)

    # data.write_csv("test.csv")


if __name__ == "__main__":
    write_db_from_csv(
        table_name="membership_count",
        db_uri=connection_uri,
    )
