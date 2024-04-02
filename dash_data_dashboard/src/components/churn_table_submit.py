from dash import Input, Output, State, Dash
import dash_mantine_components as dmc
import polars as pl

from .ids import Ids


def render(app: Dash) -> dmc.Button:
    """Render the submit button"""

    @app.callback(
        Output(Ids.CHURN_DATA_TABLE_SUBMIT, "n_clicks"),
        Input(Ids.CHURN_DATA_TABLE_SUBMIT, "n_clicks"),
        State(Ids.CHURN_DATA_TABLE, "data"),
        prevent_initial_call=True,
        background=True,
        running=[(Output(Ids.CHURN_DATA_TABLE_SUBMIT, "disabled"), True, False)],
    )
    def update_database(n_clicks: int, updated_data: list[dict]) -> int:
        """Update the emailed field in the database for the accts that have been selected"""

        data = pl.LazyFrame(updated_data)

        data = data.select(
            pl.col("Neon ID").alias("neon_id"), pl.col("Emailed").alias("emailed")
        )

        return n_clicks

    return dmc.Button(
        "Submit Changes",
        id=Ids.CHURN_DATA_TABLE_SUBMIT,
        color="indigo",
        variant="outline",
        radius="md",
    )
