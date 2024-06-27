"""Render the app header"""

import dash
import dash_mantine_components as dmc
from dash_auth import get_oauth
from dash_iconify import DashIconify
from .breakpoints import Breakpoint as bp


def get_user_profile_pic():
    oauth_client = get_oauth(dash.get_app())

    client = oauth_client.create_client("google-oidc")

    user = client.get("userinfo")

    # user = token.get("userinfo")

    return user


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
            dmc.Menu(
                [
                    dmc.MenuTarget(dmc.Avatar("", radius="xl", color="#2b2c6b")),
                    dmc.MenuDropdown(
                        [
                            dmc.MenuItem(
                                "Logout",
                                href="/oidc/logout",
                                refresh=True,
                                icon=DashIconify(icon="tabler:logout"),
                            )
                        ]
                    ),
                ],
                style={"cursor": "pointer"},
                trigger="hover",
            ),
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
