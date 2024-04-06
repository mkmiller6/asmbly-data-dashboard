import datetime
from dash import Input, Output, State, Dash
from sqlalchemy import update
from sqlalchemy.orm import Session
import dash_mantine_components as dmc
import polars as pl

from schema import Member
from engine import engine


from .ids import Ids


def render(app: Dash) -> dmc.Button:
    """Render the submit button"""

    @app.callback(
        Output(Ids.CHURN_DATA_TABLE_FILTER, "checked"),
        Input(Ids.CHURN_DATA_TABLE_SUBMIT, "n_clicks"),
        State(Ids.CHURN_DATA_TABLE, "data"),
        State(Ids.CHURN_DATA_TABLE_FILTER, "checked"),
        prevent_initial_call=True,
        background=True,
        running=[(Output(Ids.CHURN_DATA_TABLE_SUBMIT, "disabled"), True, False)],
    )
    def update_database(
        n_clicks: int, updated_data: list[dict], show_emailed_state: bool
    ) -> int:
        """Update the emailed field in the database for the accts that have been selected"""

        data = pl.LazyFrame(updated_data)

        data = data.select(
            pl.col("Neon ID").cast(pl.Int64).alias("neon_id"),
            pl.when(pl.col("Emailed") == "Yes")
            .then(True)
            .when(pl.col("Last Emailed").is_not_null())
            .then(True)
            .otherwise(False)
            .alias("emailed"),
            pl.when((pl.col("Last Emailed").is_null()) & (pl.col("Emailed") == "No"))
            .then(None)
            .when((pl.col("Last Emailed").is_null()) & (pl.col("Emailed") == "Yes"))
            .then(datetime.date.today())
            .otherwise(pl.col("Last Emailed").cast(pl.Date))
            .alias("last_emailed"),
        ).collect()

        print(data)

        updates = data.to_dicts()

        with Session(engine) as session:
            session.execute(update(Member), updates)

            session.commit()

        show_emailed = show_emailed_state
        if data.get_column("emailed").any():
            show_emailed = True

        return show_emailed

    return dmc.Button(
        "Submit Changes",
        id=Ids.CHURN_DATA_TABLE_SUBMIT,
        color="indigo",
        variant="outline",
        radius="md",
    )
