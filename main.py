"""Run the Dash app"""

import os
from dash import Dash, CeleryManager
from celery import Celery
from dash_auth import OIDCAuth
from dash_data_dashboard.src.components.layout import create_layout

APP_TITLE = "Data Dashboard"
DATA_PATH = "./dash_data_dashboard/src/data/asmbly_churn_risk.csv"


# def serve_layout():
#     return create_layout(geojson)


celery_app = Celery(
    __name__,
    broker=os.environ["REDIS_URL"],
    backend=os.environ["REDIS_URL"],
)

callback_manager = CeleryManager(celery_app)

app = Dash(
    __name__,
    assets_folder="dash_data_dashboard/assets",
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
    background_callback_manager=callback_manager,
)
auth = OIDCAuth(app, secret_key=os.environ["DASH_OIDC_SECRET"])
auth.register_provider(
    "google-oidc",
    token_endpoint_auth_method="client_secret_post",
    client_id=os.environ["OIDC_CLIENT_ID"],
    client_secret=os.environ["OIDC_CLIENT_SECRET"],
    server_metadata_url=os.environ["OIDC_DISCOVERY_DOC"],
)

app.title = APP_TITLE
app.layout = create_layout()

server = app.server


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
