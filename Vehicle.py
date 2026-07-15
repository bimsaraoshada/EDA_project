from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt

# Import the Western Province EV dataset
project_dir = Path(__file__).resolve().parent
data_path = project_dir / "Western_Province_Data.xlsx"

df = pd.read_excel(data_path)

# ------------------------------
# 1) Pie chart: Vehicle category distribution
# ------------------------------
category_counts = df["Vehicle Category"].dropna().value_counts()


explode = [0.05 if i < 2 else 0 for i in range(len(category_counts))]


def autopct_func(pct):
    return f"{pct:.1f}%" if pct >= 1 else ""

plt.figure(figsize=(12, 8))
wedges, texts, autotexts = plt.pie(
    category_counts,
    labels=None,
    autopct=autopct_func,
    startangle=90,
    explode=explode,
    #shadow=True,
    shadow=False,
    radius=1.5,
    pctdistance=0.62,
    textprops={"fontsize": 13, "color": "white", "weight": "bold"},
    wedgeprops={"edgecolor": "white", "linewidth": 1.2},
)

plt.legend(
    wedges,
    category_counts.index,
    title="Vehicle Categories",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=12,
    title_fontsize=13,
    frameon=False,
)

plt.title(
    "Distribution of Electric Vehicles by Vehicle Category\n(Western Province)",
    fontsize=18,
    fontweight="bold",
    pad=24,
)

plt.axis("equal")
plt.tight_layout()

pie_output_path = project_dir / "vehicle_category_distribution.png"
plt.savefig(pie_output_path, dpi=300, bbox_inches="tight")

# ------------------------------
# 2) Horizontal bar chart: Manufacturer distribution
# ------------------------------
manufacturer_counts = df["Make"].dropna().astype(str).str.strip()
manufacturer_counts = manufacturer_counts[manufacturer_counts != ""]

# Keep the top manufacturers for a clear chart
manufacturer_top = manufacturer_counts.value_counts().head(10)
manufacturer_top = manufacturer_top.sort_values(ascending=True)

plt.figure(figsize=(10, 8))
manufacturer_top.plot(kind="barh", color="steelblue", edgecolor="black")
plt.title("Manufacturer Distribution of Electric Vehicles\n(Western Province)", fontsize=14, fontweight="bold")
plt.xlabel("Number of Vehicles")
plt.ylabel("Manufacturer")
plt.tight_layout()

bar_output_path = project_dir / "manufacturer_distribution.png"
plt.savefig(bar_output_path, dpi=300, bbox_inches="tight")

# ------------------------------
# 3) Histogram: Vehicle age distribution
# ------------------------------
# Vehicle Age = 2025 - Manufacture Year
current_year = 2025
df["Vehicle Age"] = current_year - pd.to_numeric(df["Manufacture Year"], errors="coerce")

age_data = df["Vehicle Age"].dropna()

plt.figure(figsize=(10, 8))
plt.hist(age_data, bins=15, color="mediumseagreen", edgecolor="black")
plt.title("Vehicle Age Distribution of Electric Vehicles\n(Western Province)", fontsize=14, fontweight="bold")
plt.xlabel("Vehicle Age (Years)")
plt.ylabel("Number of Vehicles")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()

age_output_path = project_dir / "vehicle_age_distribution.png"
plt.savefig(age_output_path, dpi=300, bbox_inches="tight")

# ------------------------------
# 4) Grouped bar chart: Manufacturer vs Manufacture Year
# ------------------------------
# Convert manufacture year to numeric and drop missing values
# Group the data by manufacturer and manufacture year to count vehicles
# Keep the top 10 manufacturers by total vehicle count
# Sort years in ascending order for a clear chronological comparison

plot_df = df.copy()
plot_df["Manufacture Year"] = pd.to_numeric(plot_df["Manufacture Year"], errors="coerce")
plot_df = plot_df.dropna(subset=["Make", "Manufacture Year"])

manufacturer_totals = plot_df.groupby("Make").size().sort_values(ascending=False)
top_manufacturers = manufacturer_totals.head(10).index
plot_df = plot_df[plot_df["Make"].isin(top_manufacturers)]

pivot_table = (
    plot_df.groupby(["Make", "Manufacture Year"])
    .size()
    .unstack(fill_value=0)
    .sort_index(axis=1)
)

# Ensure the columns are ordered by year ascending and select only the top manufacturers
pivot_table = pivot_table.loc[top_manufacturers]

plt.figure(figsize=(14, 8))
ax = pivot_table.plot(kind="bar", figsize=(14, 8), width=0.8)

# Add title, labels, and formatting for publication quality
ax.set_title("Electric Vehicles by Manufacturer and Manufacture Year (Western Province)", fontsize=16, fontweight="bold")
ax.set_xlabel("Manufacturer")
ax.set_ylabel("Number of Vehicles")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=0.6)

# Move the legend to the right side and make it clear
ax.legend(title="Manufacture Year", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
plt.tight_layout()

grouped_output_path = project_dir / "manufacturer_year_grouped_bar.png"
plt.savefig(grouped_output_path, dpi=300, bbox_inches="tight")
plt.show()

# ------------------------------
# 5) Grouped bar chart: Manufacturer vs Vehicle Category
# ------------------------------
# Group the data by manufacturer and vehicle category, then count vehicles
# Keep only the top 10 manufacturers by total count for a cleaner chart
# Use a different color for each category and label each bar with its value

category_plot_df = df.copy()
category_plot_df = category_plot_df.dropna(subset=["Make", "Vehicle Category"])

manufacturer_totals_cat = category_plot_df.groupby("Make").size().sort_values(ascending=False)
top_manufacturers_cat = manufacturer_totals_cat.head(10).index
category_plot_df = category_plot_df[category_plot_df["Make"].isin(top_manufacturers_cat)]

pivot_category = (
    category_plot_df.groupby(["Make", "Vehicle Category"])
    .size()
    .unstack(fill_value=0)
)

# Reorder to keep the manufacturers in the same order as the top list
pivot_category = pivot_category.loc[top_manufacturers_cat]

plt.figure(figsize=(14, 8))
ax2 = pivot_category.plot(kind="bar", figsize=(14, 8), width=0.8)

ax2.set_title("Electric Vehicles by Manufacturer and Vehicle Category (Western Province)", fontsize=16, fontweight="bold")
ax2.set_xlabel("Manufacturer")
ax2.set_ylabel("Number of Vehicles")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right")
ax2.grid(axis="y", linestyle="--", alpha=0.5)

# Place the legend outside the figure on the right
ax2.legend(title="Vehicle Category", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

# Add value labels on each bar
for container in ax2.containers:
    ax2.bar_label(container, fmt="%.0f", padding=3, fontsize=8)

plt.tight_layout()

category_output_path = project_dir / "manufacturer_category_grouped_bar.png"
plt.savefig(category_output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Pie chart saved to: {pie_output_path}")
print(f"Bar chart saved to: {bar_output_path}")
print(f"Histogram saved to: {age_output_path}")
print(f"Grouped bar chart saved to: {grouped_output_path}")
print(f"Manufacturer-category grouped bar chart saved to: {category_output_path}")

