"""Dash Data Table containing member info and ranked churn risk"""

import polars as pl
from dash import html, Dash, dash_table, Input, Output
import dash_mantine_components as dmc
from .ids import Ids

PAGE_SIZE = 15


def render(app: Dash, source: pl.LazyFrame) -> html.Div:
    """Render the churn risk table"""

    @app.callback(
        Output(Ids.CHURN_DATA_TABLE, "data"),
        Output(Ids.CHURN_DATA_TABLE, "columns"),
        Input(Ids.CHURN_DATA_TABLE, "page_current"),
        Input(Ids.CHURN_DATA_TABLE, "page_size"),
        Input(Ids.CHURN_DATA_TABLE_FILTER, "checked"),
        Input(Ids.CHURN_DATA_TABLE_SORT_BY, "value"),
        Input(Ids.CHURN_DATA_TABLE_SORT_DIR, "value"),
    )
    def update_churn_table(
        page_current: int,
        page_size: int,
        show_emailed: bool,
        sort_by: str,
        sort_dir: str,
    ) -> html.Div:

        filtered_source = (
            source.sort(pl.col(sort_by), descending=sort_dir == "desc").collect().lazy()
        )
        if not show_emailed:
            filtered_source = filtered_source.filter(pl.col("Emailed") is False)

        filtered_source = filtered_source.slice(
            offset=page_current * page_size, length=page_size
        ).collect()

        data = filtered_source.to_dicts()

        cols = [{"name": i, "id": i} for i in filtered_source.columns]

        return data, cols

    return html.Div(
        id=Ids.CHURN_DATA_TABLE_CONTAINER,
        children=[
            html.H3("Churn Risk Table"),
            dmc.Group(
                position="left",
                children=[
                    dmc.Switch(
                        id=Ids.CHURN_DATA_TABLE_FILTER,
                        label="Show members who have been emailed",
                        color="indigo",
                        checked=True,
                        mb="10px",
                    ),
                    dmc.Select(
                        id=Ids.CHURN_DATA_TABLE_SORT_BY,
                        placeholder="Sort by",
                        label="Sort by",
                        value="Churn Risk",
                        data=[
                            {"value": "Churn Risk", "label": "Churn Risk"},
                            {"value": "Name", "label": "Name"},
                            {"value": "Email Address", "label": "Email Address"},
                            {"value": "Emailed", "label": "Emailed"},
                            {"value": "Neon ID", "label": "Neon ID"},
                        ],
                        style={
                            "width": "200px",
                            "marginBottom": "10px",
                            "marginLeft": "10px",
                        },
                    ),
                    dmc.Select(
                        id=Ids.CHURN_DATA_TABLE_SORT_DIR,
                        placeholder="Sort direction",
                        label="Sort direction",
                        value="desc",
                        data=[
                            {"value": "asc", "label": "Asc"},
                            {"value": "desc", "label": "Desc"},
                        ],
                        style={
                            "width": "200px",
                            "marginBottom": "10px",
                            "marginLeft": "10px",
                        },
                    ),
                ],
                m="10px",
            ),
            dash_table.DataTable(
                id=Ids.CHURN_DATA_TABLE,
                page_current=0,
                page_size=PAGE_SIZE,
                page_action="custom",
                editable=True,
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
                row_selectable="multi",
            ),
        ],
    )
