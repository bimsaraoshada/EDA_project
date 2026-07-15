import pandas as pd

df = pd.read_excel("charging_centers_with_coordinates.xlsx")

import geopandas as gpd

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),
    crs="EPSG:4326"
)
import geopandas as gpd

# Change this to the correct path if needed
shapefile = "lka_admin_boundaries.shp"

boundaries = gpd.read_file(shapefile, layer="lka_admin3")

print("Loaded successfully!")
print(boundaries.columns.tolist())
print(boundaries.head())

import pandas as pd

df = pd.read_excel("charging_centers_with_coordinates.xlsx")

print(df.sort_values("Longitude", ascending=False)[
    ["Station Name",
     "Divisional Secretary's Division",
     "Latitude",
     "Longitude"]
].head(10))

import geopandas as gpd
df = df[
    (df["Longitude"] >= 79.7) &
    (df["Longitude"] <= 80.35) &
    (df["Latitude"] >= 6.0) &
    (df["Latitude"] <= 7.5)
]

stations = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),
    crs="EPSG:4326"
)

western = boundaries[
    boundaries["adm1_name"] == "Western"
]

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 12))

# Draw DS Division boundaries
western.plot(
    ax=ax,
    color="#F8F8F8",
    edgecolor="gray",
    linewidth=0.8
)

# Plot charging stations
stations.plot(
    ax=ax,
    color="#D62728",
    markersize=45,
    marker="o",
    edgecolor="black",
    linewidth=0.4,
    alpha=0.9,
    label="Existing EV Charging Stations"
)

plt.title(
    "Spatial Distribution of Existing EV Charging Stations\nWestern Province, Sri Lanka",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.legend(loc="lower left")

plt.axis("off")

plt.tight_layout()

plt.subplots_adjust(top=0.90)

plt.savefig(
    "Existing_EV_Charging_Stations_Western_Province.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
