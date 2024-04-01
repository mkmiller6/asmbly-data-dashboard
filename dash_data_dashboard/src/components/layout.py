"""Create the layout for the dashboard"""

import polars as pl
from dash import html, Dash
import dash_mantine_components as dmc
from . import churn_risk_table, header


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
            header.render(app),
            dmc.Grid(
                mt=75,
                gutter="md",
                mx=20,
                className="grid-container",
                children=[
                    dmc.Col(
                        span=8,
                        children=[
                            churn_risk_table.render(app, source),
                        ],
                    )
                ],
            ),
        ],
    )
