"""Run the Dash app"""

from dash import Dash
from dash_data_dashboard.src.components.layout import create_layout
from dash_data_dashboard.src.data.dash.loader import load_churn_data
from pathlib import Path

APP_TITLE = "Asmbly Data Dashboard"
DATA_PATH = "./dash_data_dashboard/src/data/asmbly_churn_risk.csv"
CURRENT_PATH = Path(__file__).parents[0]


def main() -> None:
    """Run the Dash app"""
    data = load_churn_data(DATA_PATH)

    app = Dash(
        __name__,
        assets_folder="dash_data_dashboard/assets",
        external_stylesheets=[
            # include google fonts
            "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
        ],
    )
    app.title = APP_TITLE
    app.layout = create_layout(app, data)

    app.run(debug=True)


if __name__ == "__main__":
    main()
