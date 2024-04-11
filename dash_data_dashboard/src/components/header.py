"""Render the app header"""

import dash
import dash_mantine_components as dmc
from .breakpoints import Breakpoint as bp


def create_header_content() -> dmc.Group:
    """Create the header content"""

    return dmc.Group(
        spacing="xl",
        position="apart",
        w="100%",
        children=[
            dmc.Group(
                children=[
                    dmc.Anchor(
                        dmc.Image(
                            src="https://asmbly.org/wp-content/uploads/2023/12/purple-horizontal.svg",
                            fit="contain",
                            width=130,
                        ),
                        href="https://asmbly.org",
                        target="_blank",
                    ),
                    dmc.Title(
                        dash.get_app().title,
                        order=2,
                        weight=500,
                        color="#2b2c6b",
                    ),
                ],
                spacing="xl",
                position="left",
            ),
            dmc.Avatar("MM", radius="xl", color="#2b2c6b"),
        ],
    )


def render() -> dmc.Header:
    """Render the app header"""

    return dmc.Header(
        height=70,
        px=25,
        fixed=True,
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        },
        children=[
            dmc.MediaQuery(
                create_header_content(),
                smallerThan="md",
                styles={"display": "none"},
                innerBoxStyle={"width": bp.xxl},
            ),
            dmc.MediaQuery(
                create_header_content(),
                largerThan="md",
                styles={"display": "none"},
                innerBoxStyle={"width": "100%"},
            ),
        ],
    )
