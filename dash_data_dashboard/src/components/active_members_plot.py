import datetime
import plotly.express as px
import dash_mantine_components as dmc
import polars as pl
from dash import Input, Output, Dash, dcc, html
from .ids import Ids
from . import active_members_plot_date_range


def render(app: Dash, source: pl.LazyFrame) -> dmc.Card:
    """Render the active members plot"""

    @app.callback(
        Output(Ids.ACTIVE_MEMBERS_PLOT, "figure"),
        Input(Ids.ACTIVE_MEMBERS_PLOT_DATE_RANGE, "value"),
    )
    def update_plot(date_range: list[datetime.date]) -> html.Div:
        """Update the plot"""

        min_date = datetime.date.fromisoformat(date_range[0])
        max_date = datetime.date.fromisoformat(date_range[1])

        data = (
            source.filter(
                pl.col("date").is_between(min_date, max_date, closed="both"),
                pl.col("total_active_count") > 0,
            )
            .sort(by="date")
            .select(
                pl.col("total_active_count").alias("count"),
                pl.col("date").cast(pl.Date),
            )
        )

        serialized_dates = (
            data.select((pl.col("date").dt.epoch("d")).alias("x")).collect().to_series()
        )

        dates = data.select("date").collect().to_series()

        fig = px.line(
            x=dates,
            y=data.select("count").collect().to_series(),
            labels={
                "x": "Date",
                "y": "Active Paying Members",
            },
            markers=True,
        )

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
        )

        return (dcc.Graph(id=Ids.ACTIVE_MEMBERS_PLOT, figure=fig),)

    return dmc.Card(
        radius="md",
        shadow="md",
        withBorder=True,
        children=[
            dmc.Text(
                "Active Members Over Time",
                size="lg",
            ),
            dmc.Divider(),
            active_members_plot_date_range.render(),
            dcc.Graph(id=Ids.ACTIVE_MEMBERS_PLOT),
        ],
    )
