"""Run the Dash app"""

import os
from dash import Dash, CeleryManager, DiskcacheManager
from dash_data_dashboard.src.components.layout import create_layout
from dash_data_dashboard.src.data.dash.loader import load_churn_data
from celery import Celery
import diskcache

APP_TITLE = "Asmbly Data Dashboard"
DATA_PATH = "./dash_data_dashboard/src/data/asmbly_churn_risk.csv"


celery_app = Celery(
    __name__,
    broker=os.environ["REDIS_URL"],
    backend=os.environ["REDIS_URL"],
)

disk_cache = diskcache.Cache("./cache")

callback_manager = CeleryManager(celery_app)

# callback_manager = DiskcacheManager(disk_cache)


data = load_churn_data(DATA_PATH)

app = Dash(
    __name__,
    assets_folder="dash_data_dashboard/assets",
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
    background_callback_manager=callback_manager,
)
app.title = APP_TITLE
app.layout = create_layout(app, data)

server = app.server


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
