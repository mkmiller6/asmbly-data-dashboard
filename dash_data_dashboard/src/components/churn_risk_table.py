"""Dash Data Table containing member info and ranked churn risk"""

import math
import polars as pl
from dash import html, Dash, dash_table, Input, Output
import dash_mantine_components as dmc
from .ids import Ids
from . import (
    churn_table_sort_direction,
    churn_table_sort_by,
    churn_table_emailed_toggle,
    churn_table_search,
    churn_table_submit,
)

PAGE_SIZE = 15


def render(app: Dash, source: pl.LazyFrame) -> html.Div:
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

        filtered_source = source.sort(
            pl.col(sort_by), descending=sort_dir == "desc"
        ).filter(
            pl.col("Name").str.to_lowercase().str.contains(search, literal=True)
            | pl.col("Email Address").str.contains(search, literal=True)
            | pl.col("Neon ID").str.contains(search, literal=True)
        )
        if not show_emailed:
            filtered_source = filtered_source.filter(pl.col("Emailed") == "No")

        final_df = filtered_source.slice(
            offset=page_current * page_size, length=page_size
        ).collect()

        data = final_df.to_dicts()

        cols = [
            {"name": i, "id": i}
            for i in filtered_source.select(pl.all().exclude("Emailed")).columns
        ]

        cols.append(
            {
                "name": "Emailed",
                "id": "Emailed",
                "presentation": "dropdown",
            }
        )

        items = filtered_source.select(pl.len()).collect().item()

        page_count = 1 if items == 0 else math.ceil(items / PAGE_SIZE)

        return data, cols, page_count

    return html.Div(
        id=Ids.CHURN_DATA_TABLE_CONTAINER,
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
