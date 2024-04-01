"""Render the app header"""

import dash_mantine_components as dmc
from dash import Dash, html
from .breakpoints import Breakpoint as bp


def create_header_content(app: Dash) -> dmc.Group:
    """Create the header content"""

    return dmc.Group(
        spacing="xl",
        position="apart",
        w="100%",
        children=[
            dmc.Text(
                app.title,
                size="xl",
                weight=500,
                color="#2b2c6b",
            ),
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
                position="right",
            ),
        ],
    )


def render(app: Dash) -> dmc.Header:
    """Render the app header"""

    return dmc.Header(
        height=70,
        px=25,
        fixed=True,
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
        },
        children=[
            dmc.MediaQuery(
                create_header_content(app),
                smallerThan="md",
                styles={"display": "none"},
                innerBoxStyle={"width": bp.xxl},
            ),
            dmc.MediaQuery(
                create_header_content(app),
                largerThan="md",
                styles={"display": "none"},
                innerBoxStyle={"width": "100%"},
            ),
        ],
    )
