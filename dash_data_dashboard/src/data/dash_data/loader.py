"""
Data loading functions
"""

import polars as pl


def load_churn_data(path: str) -> pl.LazyFrame:
    """Load data from CSV file"""

    q = pl.scan_csv(path).select(
        pl.col("neon_id").alias("Neon ID"),
        (
            pl.col("first_name").str.to_titlecase()
            + " "
            + pl.col("last_name").str.to_titlecase()
        ).alias("Name"),
        pl.col("email").str.to_lowercase().alias("Email Address"),
        pl.col("risk_score").round(2).alias("Churn Risk"),
    )

    return q


def load_membership_data(db_uri: str) -> pl.LazyFrame:
    """Load data from database"""

    query = """
        SELECT *
        FROM membership_count
        ORDER BY date DESC
    """

    lf = pl.read_database_uri(query, db_uri).lazy()

    return lf
