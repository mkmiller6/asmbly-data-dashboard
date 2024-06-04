import datetime
import plotly.graph_objects as go
import dash_mantine_components as dmc
import polars as pl
from dash import dcc, Input, Output, callback
from .ids import Ids
from . import churns_and_join_plot_avg


def render(source: pl.LazyFrame) -> dmc.Card:
    """Render the active members plot"""

    @callback(
        Output(Ids.CHURNS_AND_JOINS_PLOT, "figure"),
        Input(Ids.CHURNS_AND_JOINS_PLOT_AVG, "value"),
    )
    def update_churns_and_joins_plot(average_selection: str):

        match average_selection:
            case "7 Days":
                avg = "7d"
            case "14 Days":
                avg = "14d"
            case "30 Days":
                avg = "30d"
            case "90 Days":
                avg = "90d"
            case _:
                avg = None

        data = source.sort(by="date").select(
            pl.col("date").cast(pl.Date),
            pl.col("churn_count"),
            pl.col("member_signups_count"),
            pl.col("acct_signups_count"),
        )

        if avg:
            data = (
                source.sort(by="date")
                .rolling("date", period=avg, closed="none")
                .agg(
                    pl.col("churn_count").mean().alias("churn_count"),
                    pl.col("member_signups_count").mean().alias("member_signups_count"),
                    pl.col("acct_signups_count").mean().alias("acct_signups_count"),
                )
            )

        dates = data.select("date").collect().to_series()

        date_range = [
            dates.min() - datetime.timedelta(days=5),
            dates.max() + datetime.timedelta(days=5),
        ]

        trace1 = go.Scatter(
            x=dates,
            y=data.select("churn_count").collect().to_series(),
            mode="lines",
            name="Churns",
            marker=dict(color="#d62728"),
        )
        trace2 = go.Scatter(
            x=dates,
            y=data.select("member_signups_count").collect().to_series(),
            mode="lines",
            name="Membership Signups",
            marker=dict(color="#2ca02c"),
        )
        trace3 = go.Scatter(
            x=dates,
            y=data.select("acct_signups_count").collect().to_series(),
            mode="lines",
            name="Neon Account Signups",
            marker=dict(color="#1f77b4"),
        )

        data = [trace1, trace2, trace3]

        layout = dict(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all"),
                        ]
                    ),
                    yanchor="bottom",
                    y=1.17,
                ),
                rangeslider=dict(visible=True),
                range=date_range,
                type="date",
                title="Date",
            ),
            yaxis=dict(
                title="Count",
            ),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.01
            ),
        )

        fig = dict(data=data, layout=layout)

        return fig

    return dmc.Card(
        radius="md",
        shadow="md",
        withBorder=True,
        children=[
            dmc.Text(
                "Churns and Signups",
                size="lg",
                mb=15,
            ),
            dmc.Divider(mb=15),
            churns_and_join_plot_avg.render(),
            dcc.Graph(id=Ids.CHURNS_AND_JOINS_PLOT),
        ],
    )
