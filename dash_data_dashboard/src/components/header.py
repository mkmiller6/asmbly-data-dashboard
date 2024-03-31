"""Render the app header"""

import dash_mantine_components as dmc
from dash import Dash, html


def render(app: Dash) -> dmc.Header:
    """Render the app header"""

    return dmc.Header(
        height=75,
        p="lg",
        children=[
            dmc.Group(
                children=[
                    dmc.Text(app.title, size="xl", weight=500, color="#2b2c6b"),
                    dmc.Group(
                        children=[
                            html.A(
                                dmc.Avatar(
                                    src="https://asmbly.org/wp-content/uploads/2023/12/purple-horizontal.svg",
                                    radius="xl",
                                ),
                                href="https://asmbly.org",
                                target="_blank",
                            ),
                            dmc.Avatar("MM", radius="xl", color="#2b2c6b"),
                        ],
                        spacing="xl",
                    ),
                ],
                position="apart",
            ),
        ],
        fixed=False,
    )
