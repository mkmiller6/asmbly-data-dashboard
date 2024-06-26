import datetime
import polars as pl
import dash_mantine_components as dmc


def render(source: pl.LazyFrame) -> dmc.Card:
    """Render the churns and joins card"""

    today = (
        source.filter(
            pl.col("date") == pl.lit(datetime.date.today() - datetime.timedelta(days=1))
        )
        .select(
            pl.col("member_signups_count"),
            pl.col("churn_count"),
            pl.col("acct_signups_count"),
        )
        .collect()
    )

    if today.is_empty():
        today = source.select(
            pl.col("member_signups_count").first(),
            pl.col("churn_count").first(),
            pl.col("acct_signups_count").first(),
        ).collect()

    mem_signups = today.get_column("member_signups_count").item()

    churns = today.get_column("churn_count").item()

    acct_signups = today.get_column("acct_signups_count").item()

    return dmc.Card(
        withBorder=True,
        radius="md",
        shadow="md",
        style={
            "flex": "1",
            "display": "flex",
            "flexDirection": "column",
        },
        children=[
            dmc.Stack(
                children=[
                    dmc.Text(
                        "Daily Membership Changes",
                        size="lg",
                        align="center",
                        style={"flex": "0"},
                    ),
                    dmc.Divider(style={"flex": "0"}),
                    dmc.Stack(
                        children=[
                            dmc.Text(
                                f"Membership Signups: {mem_signups:,}", align="center"
                            ),
                            dmc.Space(),
                            dmc.Text(f"Churned Accounts: {churns:,}", align="center"),
                            dmc.Space(),
                            dmc.Text(
                                f"Account Signups: {acct_signups:,}", align="center"
                            ),
                        ],
                        spacing="lg",
                        justify="center",
                        align="center",
                        style={"flex": "1"},
                    ),
                ],
                style={"flex": "1"},
            )
        ],
    )
