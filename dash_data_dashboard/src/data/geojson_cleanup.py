import json
import polars as pl


with open(
    "./dash_data_dashboard/src/data/tx_texas_zip_codes_geo.min.reduced.json",
    "r",
    encoding="utf-8",
) as f:
    geojson = json.load(f)

new_geo = {
    "type": "FeatureCollection",
    "features": [],
}

zips = (
    pl.read_csv(
        "./dash_data_dashboard/src/data/zips.csv", has_header=False, dtypes=[pl.Int64]
    )
    .transpose()
    .lazy()
)

for feature in geojson["features"]:

    exists = (
        zips.filter(
            pl.col("column_0")
            == pl.lit(feature["properties"]["ZCTA5CE10"], dtype=pl.Int64)
        )
        .count()
        .collect()
        .get_column("column_0")
        .item()
    )

    if exists > 0:

        new_feature = {
            "type": "Feature",
            "properties": {
                "ZCTA5CE10": feature["properties"]["ZCTA5CE10"],
            },
            "geometry": feature["geometry"],
        }

        new_geo["features"].append(new_feature)


with open(
    "./dash_data_dashboard/src/data/tx_zip_codes_geo_min.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(new_geo, f)
