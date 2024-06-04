import datetime
import plotly.express as px
import dash_mantine_components as dmc
import polars as pl
from dash import dcc
from .ids import Ids


def render(source: pl.LazyFrame) -> dmc.Card:
    """Render the active members plot"""

    data = (
        source.filter(
            pl.col("total_active_count") > 0,
        )
        .sort(by="date")
        .select(
            pl.col("total_active_count").alias("count"),
            pl.col("date"),
        )
    )

    serialized_dates = (
        data.select((pl.col("date").dt.epoch("d")).alias("x")).collect().to_series()
    )

    dates = data.select("date").collect().to_series()

    date_range = [
        dates.min() - datetime.timedelta(days=5),
        dates.max() + datetime.timedelta(days=5),
    ]

    fig = px.line(
        x=dates,
        y=data.select("count").collect().to_series(),
        labels={
            "x": "Date",
            "y": "Active Paying Members",
        },
        markers=False,
    )

    fig.update_traces(line_color="#1f77b4")

    fig.update_layout(plot_bgcolor="white")

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        range=date_range,
        gridcolor="lightgrey",
        showline=True,
        linecolor="black",
        ticks="outside",
        tickcolor="lightgrey",
    )

    fig.update_yaxes(gridcolor="lightgrey", autorange=True, fixedrange=False)

    return dmc.Card(
        radius="md",
        shadow="md",
        withBorder=True,
        children=[
            dmc.Text(
                "Active Members Over Time",
                size="lg",
                mb=15,
            ),
            dmc.Divider(mb=15),
            dcc.Graph(id=Ids.ACTIVE_MEMBERS_PLOT, figure=fig),
        ],
    )
