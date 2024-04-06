import datetime
import polars as pl
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from .ids import Ids


def render(source: pl.LazyFrame) -> dmc.Card:
    """Render the active members card"""

    active_yesterday = (
        source.select(
            pl.col("total_active_count").filter(
                pl.col("date")
                == pl.lit(datetime.date.today() - datetime.timedelta(days=1))
            )
        )
        .collect()
        .get_column("total_active_count")
        .item()
    )
    active_two_days_ago = (
        source.select(
            pl.col("total_active_count").filter(
                pl.col("date")
                == pl.lit(datetime.date.today() - datetime.timedelta(days=2))
            )
        )
        .collect()
        .get_column("total_active_count")
        .item()
    )

    active_month_ago = (
        source.select(
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
        source.select(
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

    daily_change = active_yesterday - active_two_days_ago

    return dmc.Card(
        id=Ids.ACTIVE_MEMBERS_CARD,
        withBorder=True,
        radius="md",
        shadow="md",
        children=[
            dmc.Text("Active Membership", size="lg", align="center", mb=15),
            dmc.Divider(),
            dmc.Stack(
                children=[
                    dmc.Stack(
                        [
                            dmc.Text("Current (+/- yesterday)"),
                            (
                                dmc.Text(
                                    f"{active_yesterday:,} ({daily_change:+})",
                                    color="green",
                                    weight=500,
                                )
                                if daily_change >= 0
                                else dmc.Text(
                                    f"{active_yesterday:,} ({daily_change:+})",
                                    color="red",
                                    weight=500,
                                )
                            ),
                        ],
                        align="center",
                        mt=15,
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
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    height=25,
                                                    color="green",
                                                ),
                                            ]
                                            if mom_change_percent > 0
                                            else [
                                                dmc.Text(
                                                    f"{mom_change_percent:.2f}%",
                                                    color="red",
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    height=25,
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
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    height=25,
                                                    color="green",
                                                ),
                                            ]
                                            if mom_change_count > 0
                                            else [
                                                dmc.Text(
                                                    f"{mom_change_count:,}",
                                                    color="red",
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    height=25,
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
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    height=25,
                                                    color="green",
                                                ),
                                            ]
                                            if yoy_change_percent > 0
                                            else [
                                                dmc.Text(
                                                    f"{yoy_change_percent:.2f}%",
                                                    color="red",
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    height=25,
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
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-up-line-duotone",
                                                    height=25,
                                                    color="green",
                                                ),
                                            ]
                                            if yoy_change_count > 0
                                            else [
                                                dmc.Text(
                                                    f"{yoy_change_count:,}",
                                                    color="red",
                                                    weight=500,
                                                ),
                                                DashIconify(
                                                    icon="solar:double-alt-arrow-down-line-duotone",
                                                    height=25,
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
                spacing="lg",
                mb=20,
            ),
        ],
    )
