import datetime
import polars as pl
from dash import html, Dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from engine import raw_uri
from .ids import Ids


def render(app: Dash, source: pl.LazyFrame) -> dmc.Card:
    """Render the active members card"""

    query = """
        SELECT total_active_count, date
        FROM membership_count
        WHERE date > (CURRENT_DATE - INTERVAL '366 days')
    """

    data = pl.read_database_uri(query, raw_uri).lazy()

    active_yesterday = (
        data.select(
            pl.col("total_active_count").filter(
                pl.col("date")
                == pl.lit(datetime.date.today() - datetime.timedelta(days=1))
            )
        )
        .collect()
        .get_column("total_active_count")
        .item()
    )

    active_month_ago = (
        data.select(
            pl.col("total_active_count").filter(
                pl.col("date")
                == pl.lit(datetime.date.today() - datetime.timedelta(days=30))
            )
        )
        .collect()
        .get_column("total_active_count")
        .item()
    )

    active_year_ago = (
        data.select(
            pl.col("total_active_count").filter(
                pl.col("date")
                == pl.lit(datetime.date.today() - datetime.timedelta(days=365))
            )
        )
        .collect()
        .get_column("total_active_count")
        .item()
    )

    mom_change_percent = ((active_yesterday / active_month_ago) - 1) * 100
    yoy_change_percent = ((active_yesterday / active_year_ago) - 1) * 100

    mom_change_count = active_yesterday - active_month_ago
    yoy_change_count = active_yesterday - active_year_ago

    return dmc.Card(
        id=Ids.ACTIVE_MEMBERS_CARD,
        withBorder=True,
        radius="md",
        shadow="md",
        children=[
            dmc.Stack(
                children=[
                    dmc.Text("Membership", size="lg", align="center"),
                    dmc.Divider(),
                    dmc.Stack(
                        [
                            dmc.Text("Current Active Members"),
                            dmc.Text(f"{active_yesterday:,}"),
                        ],
                        align="center",
                    ),
                    dmc.Divider(),
                    dmc.Text("Month-over-Month Change", align="center"),
                    dmc.Group(
                        children=[
                            dmc.Stack(
                                [
                                    dmc.Text("Percent"),
                                    dmc.Group(
                                        (
                                            [
                                                dmc.Text(
                                                    f"{mom_change_percent:.2f}%",
                                                    color="green",
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    color="green",
                                                ),
                                            ]
                                            if mom_change_percent > 0
                                            else [
                                                dmc.Text(
                                                    f"{mom_change_percent:.2f}%",
                                                    color="red",
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    color="red",
                                                ),
                                            ]
                                        ),
                                        spacing="sm",
                                        align="center",
                                    ),
                                ],
                                spacing="sm",
                                align="center",
                            ),
                            dmc.Stack(
                                [
                                    dmc.Text("Count"),
                                    dmc.Group(
                                        (
                                            [
                                                dmc.Text(
                                                    f"{mom_change_count:,}",
                                                    color="green",
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    color="green",
                                                ),
                                            ]
                                            if mom_change_count > 0
                                            else [
                                                dmc.Text(
                                                    f"{mom_change_count:,}", color="red"
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    color="red",
                                                ),
                                            ]
                                        ),
                                        spacing="sm",
                                        align="center",
                                    ),
                                ],
                                spacing="sm",
                                align="center",
                                justify="center",
                            ),
                        ],
                        spacing="sm",
                        align="center",
                        position="apart",
                        mx=50,
                    ),
                    dmc.Divider(),
                    dmc.Text("Year-over-Year Change", align="center"),
                    dmc.Group(
                        children=[
                            dmc.Stack(
                                [
                                    dmc.Text("Percent"),
                                    dmc.Group(
                                        (
                                            [
                                                dmc.Text(
                                                    f"{yoy_change_percent:.2f}%",
                                                    color="green",
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    color="green",
                                                ),
                                            ]
                                            if yoy_change_percent > 0
                                            else [
                                                dmc.Text(
                                                    f"{yoy_change_percent:.2f}%",
                                                    color="red",
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    color="red",
                                                ),
                                            ]
                                        ),
                                        spacing="sm",
                                        align="center",
                                    ),
                                ],
                                spacing="sm",
                                align="center",
                                justify="center",
                            ),
                            dmc.Stack(
                                [
                                    dmc.Text("Count"),
                                    dmc.Group(
                                        (
                                            [
                                                dmc.Text(
                                                    f"{yoy_change_count:,}",
                                                    color="green",
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    color="green",
                                                ),
                                            ]
                                            if yoy_change_count > 0
                                            else [
                                                dmc.Text(
                                                    f"{yoy_change_count:,}", color="red"
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    color="red",
                                                ),
                                            ]
                                        ),
                                        spacing="sm",
                                        align="center",
                                    ),
                                ],
                                spacing="sm",
                                align="center",
                                justify="center",
                            ),
                        ],
                        spacing="sm",
                        align="center",
                        position="apart",
                        mx=50,
                    ),
                ],
            )
        ],
    )
