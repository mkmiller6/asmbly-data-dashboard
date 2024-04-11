"""Create the layout for the dashboard"""

from dash import html
import dash_mantine_components as dmc
from dash_data_dashboard.src.data.dash_data.loader import load_membership_data
from engine import raw_uri
from . import (
    churn_risk_table,
    header,
    active_members_card,
    churns_and_joins,
    active_members_plot,
)
from .breakpoints import Breakpoint as bp


def create_layout() -> html.Div:
    """Create the layout of the dashboard"""

    source = load_membership_data(raw_uri)

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
                mb=40,
                children=[
                    header.render(),
                    dmc.Grid(
                        mt=85,
                        gutter="md",
                        children=[
                            dmc.Col(
                                span=9,
                                children=[
                                    churn_risk_table.render(),
                                ],
                            ),
                            dmc.Col(
                                span=3,
                                children=[
                                    dmc.Stack(
                                        [
                                            active_members_card.render(source),
                                            churns_and_joins.render(source),
                                        ],
                                        h=796,
                                    )
                                ],
                            ),
                            dmc.Col(
                                span=12,
                                children=[active_members_plot.render(source)],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
