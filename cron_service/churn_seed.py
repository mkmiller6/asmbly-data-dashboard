"""Seed the database with the intitial member data"""

from pathlib import Path
import polars as pl

from engine import connection_uri


def load_data_from_csv(file_path: str) -> pl.DataFrame:
    """Load data from CSV file"""
    return (
        pl.scan_csv(file_path)
        .select(
            pl.col("neon_id"),
            pl.col("first_name"),
            pl.col("last_name"),
            pl.col("email"),
            pl.col("risk_score"),
            pl.col("duration").alias("membership_duration"),
        )
        .collect()
    )


def write_db_from_csv(table_name: str, file_path: str, db_uri: str) -> None:
    """Seed the database with the intitial member data"""
    data = load_data_from_csv(file_path)

    data.write_database(
        table_name=table_name, connection=db_uri, if_table_exists="append"
    )


if __name__ == "__main__":
    write_db_from_csv(
        table_name="member",
        file_path=Path()
        .cwd()
        .joinpath("dash_data_dashboard/src/data/asmbly_churn_risk.csv"),
        db_uri=connection_uri,
    )
