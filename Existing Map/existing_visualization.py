import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- Load data ---
df = pd.read_excel("charging_centers_with_coordinates.xlsx")

shapefile = "lka_admin_boundaries.shp"
boundaries = gpd.read_file(shapefile, layer="lka_admin3")

print("Loaded successfully!")
print(boundaries.columns.tolist())
print(boundaries.head())

# --- Filter to Western Province bounding box ---
df = df[
    (df["Longitude"] >= 79.7) &
    (df["Longitude"] <= 80.35) &
    (df["Latitude"] >= 6.0) &
    (df["Latitude"] <= 7.5)
]

# --- Group stations by identical (rounded) coordinates and count them ---
df["lat_round"] = df["Latitude"].round(5)
df["lon_round"] = df["Longitude"].round(5)

grouped = (
    df.groupby(["lat_round", "lon_round"])
    .agg(
        station_count=("Station Name", "count"),
        station_names=("Station Name", lambda x: ", ".join(x))
    )
    .reset_index()
    .rename(columns={"lat_round": "Latitude", "lon_round": "Longitude"})
)

stations = gpd.GeoDataFrame(
    grouped,
    geometry=gpd.points_from_xy(grouped["Longitude"], grouped["Latitude"]),
    crs="EPSG:4326"
)

western = boundaries[boundaries["adm1_name"] == "Western"]

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 12))

western.plot(
    ax=ax,
    color="#F8F8F8",
    edgecolor="gray",
    linewidth=0.8
)

max_count = stations["station_count"].max()

cmap = plt.cm.YlOrRd
norm = mcolors.Normalize(vmin=1, vmax=max_count)

scatter = ax.scatter(
    stations.geometry.x,
    stations.geometry.y,
    c=stations["station_count"],
    cmap=cmap,
    norm=norm,
    s=stations["station_count"].apply(lambda n: 60 + (n - 1) * 40),
    edgecolor="black",
    linewidth=0.5,
    alpha=0.9,
    zorder=3
)

for _, row in stations[stations["station_count"] > 1].iterrows():
    ax.annotate(
        str(row["station_count"]),
        xy=(row.geometry.x, row.geometry.y),
        ha="center", va="center",
        fontsize=8, fontweight="bold", color="white",
        zorder=4
    )

cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, pad=0.02)
cbar.set_label("Number of Charging Stations at Location", fontsize=10)

plt.title(
    "Spatial Distribution of Existing EV Charging Stations\nWestern Province, Sri Lanka",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.axis("off")
plt.tight_layout()
plt.subplots_adjust(top=0.90)

plt.savefig(
    "Existing_EV_Charging_Stations_Western_Province.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
