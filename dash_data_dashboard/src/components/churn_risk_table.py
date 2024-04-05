"""Dash Data Table containing member info and ranked churn risk"""

import math
import polars as pl
from dash import html, Dash, dash_table, Input, Output
import dash_mantine_components as dmc
from engine import raw_uri
from .ids import Ids
from . import (
    churn_table_sort_direction,
    churn_table_sort_by,
    churn_table_emailed_toggle,
    churn_table_search,
    churn_table_submit,
)


PAGE_SIZE = 15


def render(app: Dash) -> html.Div:
    """Render the churn risk table"""

    @app.callback(
        Output(Ids.CHURN_DATA_TABLE, "data"),
        Output(Ids.CHURN_DATA_TABLE, "columns"),
        Output(Ids.CHURN_DATA_TABLE, "page_count"),
        Input(Ids.CHURN_DATA_TABLE, "page_current"),
        Input(Ids.CHURN_DATA_TABLE, "page_size"),
        Input(Ids.CHURN_DATA_TABLE_FILTER, "checked"),
        Input(Ids.CHURN_DATA_TABLE_SORT_BY, "value"),
        Input(Ids.CHURN_DATA_TABLE_SORT_DIR, "value"),
        Input(Ids.CHURN_DATA_TABLE_SEARCH, "value"),
    )
    def update_churn_table(
        page_current: int,
        page_size: int,
        show_emailed: bool,
        sort_by: str,
        sort_dir: str,
        search: str,
    ) -> html.Div:

        search = search.lower()

        sort_mapping = {
            "Name": "first_name",
            "Email Address": "email",
            "Neon ID": "neon_id",
            "Churn Risk": "risk_score",
            "Emailed": "emailed",
        }

        query = f"""
        SELECT neon_id, first_name, last_name, email, risk_score, emailed, last_emailed
        FROM member
        WHERE active = true {"AND emailed = false" if not show_emailed else ""}
        ORDER BY {sort_mapping.get(sort_by, "risk_score")} {sort_dir.upper()}
        """

        uri = raw_uri

        result_df = (
            pl.read_database_uri(query, uri)
            .lazy()
            .select(
                pl.col("neon_id").alias("Neon ID"),
                (pl.col("first_name") + " " + pl.col("last_name")).alias("Name"),
                pl.col("email").alias("Email Address"),
                pl.col("risk_score").round(3).alias("Churn Risk"),
                pl.when(pl.col("emailed") == True)
                .then(pl.lit("Yes"))
                .otherwise(pl.lit("No"))
                .alias("Emailed"),
                pl.col("last_emailed").alias("Last Emailed"),
            )
            .filter(
                pl.col("Name").str.to_lowercase().str.contains(search, literal=True)
                | pl.col("Email Address").str.contains(search, literal=True)
                | pl.col("Neon ID").str.contains(search, literal=True)
            )
        )

        paged_df = result_df.slice(
            offset=page_current * page_size, length=page_size
        ).collect()

        data = paged_df.to_dicts()

        cols = [
            {"name": i, "id": i}
            for i in paged_df.select(
                pl.all().exclude(["Emailed", "Last Emailed"])
            ).columns
        ]

        append = [
            {
                "name": "Emailed",
                "id": "Emailed",
                "presentation": "dropdown",
            },
            {
                "name": "Last Emailed",
                "id": "Last Emailed",
                "type": "datetime",
                "on_change": {
                    "action": "coerce",
                    "failure": "default",
                },
                "validation": {
                    "default": None,
                },
            },
        ]
        for col in append:
            cols.append(col)

        items = result_df.select(pl.count()).collect().item()
        page_count = 1 if items == 0 else math.ceil(items / PAGE_SIZE)

        return data, cols, page_count

    return dmc.Card(
        id=Ids.CHURN_DATA_TABLE_CONTAINER,
        withBorder=True,
        shadow="md",
        radius="md",
        mih=797,
        children=[
            dmc.Text("Churn Risk", size="lg", mb="15px"),
            dmc.Divider(mb="15px"),
            dmc.Group(
                position="left",
                align="end",
                children=[
                    churn_table_sort_by.render(),
                    churn_table_sort_direction.render(),
                    churn_table_search.render(),
                    churn_table_emailed_toggle.render(),
                ],
                mb="15px",
            ),
            dash_table.DataTable(
                id=Ids.CHURN_DATA_TABLE,
                page_current=0,
                page_size=PAGE_SIZE,
                editable=True,
                tooltip_header={
                    "Last Emailed": "YYYY-MM-DD Format",
                },
                dropdown={
                    "Emailed": {
                        "options": [{"label": i, "value": i} for i in ["Yes", "No"]],
                    }
                },
                page_action="custom",
                style_table={"overflowX": "auto"},
                style_cell={
                    "whiteSpace": "normal",
                    "height": "auto",
                    "lineHeight": "15px",
                    "fontSize": "15px",
                    "fontFamily": "'Inter', sans-serif",
                    "textAlign": "left",
                },
                style_cell_conditional=[
                    {
                        "if": {"column_id": "Churn Risk"},
                        "fontFamily": "monospace",
                    }
                ],
                style_header={
                    "fontFamily": "'Inter', sans-serif",
                    "fontSize": "20px",
                },
            ),
            churn_table_submit.render(app),
        ],
    )
