"""Create the layout for the dashboard"""

import polars as pl
from dash import html, Dash
import dash_mantine_components as dmc
from . import (
    churn_risk_table,
    header,
    active_members_card,
    churns_and_joins,
    active_members_plot,
)
from .breakpoints import Breakpoint as bp


def create_layout(app: Dash, source: pl.LazyFrame) -> html.Div:
    """Create the layout of the dashboard"""

    return dmc.MantineProvider(
        theme={
            "fontFamily": "'Inter', sans-serif",
            "primaryColor": "indigo",
            "components": {
                "Button": {"styles": {"root": {"fontWeight": 400}}},
                "Alert": {"styles": {"title": {"fontWeight": 500}}},
                "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
            },
        },
        inherit=True,
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.Container(
                size=bp.xxl,
                px=10,
                children=[
                    header.render(app),
                    dmc.Grid(
                        mt=85,
                        gutter="md",
                        children=[
                            dmc.Col(
                                span=9,
                                children=[
                                    churn_risk_table.render(app),
                                ],
                            ),
                            dmc.Col(
                                span=3,
                                children=[
                                    dmc.Stack(
                                        [
                                            active_members_card.render(source),
                                            churns_and_joins.render(source),
                                        ]
                                    )
                                ],
                            ),
                            dmc.Col(
                                span=12,
                                children=[active_members_plot.render(app, source)],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
