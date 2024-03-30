"""Create the layout for the dashboard"""

import polars as pl
from dash import html, Dash
import dash_mantine_components as dmc
from . import churn_risk_table


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
            dmc.SimpleGrid(
                cols=1,
                children=[
                    churn_risk_table.render(app, source),
                ],
                m="20px",
            )
        ],
    )
