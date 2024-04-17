"""Generate a chloropleth map of member locations based on ZCTA (Zip Code Tabulation Area)"""

import json
import polars as pl
import plotly.express as px
from dash import dcc, Input, Output, Patch, callback
import dash_mantine_components as dmc
from engine import raw_uri
from .ids import Ids
from . import zcta_multiselect


query = """
        SELECT zip_code, active
        FROM member
        """

zip_codes = pl.read_database_uri(query, raw_uri).lazy()


def render() -> dmc.Card:
    """Render the chloropleth map"""

    # zipcodes = (
    #     zip_codes.groupby("zip_code")
    #     .agg(pl.col("zip_code").count().alias("count"))
    #     .select(pl.col("zip_code").alias("Zip Code"), pl.col("count"))
    #     .collect()
    #     .to_dicts()
    # )

    return dmc.Card(
        withBorder=True,
        radius="md",
        shadow="md",
        children=[
            dmc.Text(
                "Member Locations",
                size="lg",
                mb=15,
            ),
            dmc.Divider(mb=15),
            zcta_multiselect.render(),
            dcc.Graph(id=Ids.ZCTA_CHLOROPLETH),
        ],
    )


@callback(
    Output(Ids.ZCTA_CHLOROPLETH, "figure"),
    Input(Ids.ZCTA_MULTISELECT, "value"),
)
def update_chloropleth(mutliselect: list[str] | None) -> px.choropleth_mapbox:
    """Update the chloropleth map based on the clickData"""

    if mutliselect is None:
        return

    active = "active" in mutliselect
    inactive = "inactive" in mutliselect
    never_joined = "never_joined" in mutliselect

    with open(
        "./dash_data_dashboard/src/data/tx_zip_codes_geo_min.json",
        "r",
        encoding="utf-8",
    ) as f:
        geojson = json.load(f)

    zips = (
        zip_codes.filter((pl.col("active") == active) | (pl.col("active") != inactive))
        .groupby("zip_code")
        .agg(pl.col("zip_code").count().alias("count"))
        .select(pl.col("zip_code").alias("Zip Code"), pl.col("count"))
        .collect()
        .to_dicts()
    )

    fig = px.choropleth_mapbox(
        zips,
        geojson=geojson,
        featureidkey="properties.ZCTA5CE10",
        locations="Zip Code",
        color="count",
        color_continuous_scale="viridis",
        zoom=8,
        center={"lat": 30.3548, "lon": -97.6727},
        opacity=0.4,
        hover_name="Zip Code",
        hover_data=["count"],
        mapbox_style="carto-positron",
    )
    fig.update_layout(margin={"t": 30, "r": 60, "l": 10, "b": 10})

    # patched_fig["data"][0]["data_frame"] = zips

    return fig
