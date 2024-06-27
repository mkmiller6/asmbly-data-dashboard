"""Generate a chloropleth map of member locations based on ZCTA (Zip Code Tabulation Area)"""

import json
import polars as pl
import plotly.express as px
from dash import dcc, Input, Output, callback
import dash_mantine_components as dmc
from engine import raw_uri
from .ids import Ids
from . import zcta_multiselect


def render() -> dmc.Card:
    """Render the chloropleth map"""

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

    active = "active" in mutliselect
    inactive = "inactive" in mutliselect
    # never_joined = "never_joined" in mutliselect

    query = """
        SELECT zip_code, active, membership_duration
        FROM member
        """

    zip_codes = pl.read_database_uri(query, raw_uri).lazy()

    with open(
        "./dash_data_dashboard/src/data/tx_zip_codes_geo_min.json",
        "r",
        encoding="utf-8",
    ) as f:
        geojson = json.load(f)

    zips_list = []

    if active:
        active_zips = zip_codes.filter(
            (pl.col("active") == True) & (pl.col("membership_duration") > 0)
        )

        zips_list.append(active_zips)

    if inactive:
        inactive_zips = zip_codes.filter(
            (pl.col("active") == False) & (pl.col("membership_duration") > 0)
        )

        zips_list.append(inactive_zips)

    # if never_joined:
    #     never_joined_zips = zip_codes.filter(
    #         (pl.col("active") == False) & (pl.col("membership_duration") == 0)
    #     )

    #     zips_list.append(never_joined_zips)

    if zips_list:
        zips = (
            pl.concat(zips_list, how="vertical")
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
    else:
        fig = px.choropleth_mapbox(
            geojson=geojson,
            featureidkey="properties.ZCTA5CE10",
            color_continuous_scale="viridis",
            zoom=8,
            center={"lat": 30.3548, "lon": -97.6727},
            opacity=0.4,
            mapbox_style="carto-positron",
        )

    fig.update_layout(margin={"t": 30, "r": 60, "l": 10, "b": 10})

    fig.add_scattermapbox(
        lat=[30.3537],
        lon=[-97.6719],
        mode="markers",
        text=["Asmbly"],
        marker_size=12,
        marker_color="#2b2c6b",
    )

    return fig
