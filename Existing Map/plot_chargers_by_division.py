"""
plot_chargers_by_division.py

Generates a publication-quality horizontal bar chart showing the number of
EV charging stations per Divisional Secretary's (DS) Division in the
Western Province, Sri Lanka, based on the John Keells CG Auto EV charger
network dataset.

Usage (in VS Code / terminal):
    python plot_chargers_by_division.py

Requirements:
    pip install pandas openpyxl matplotlib

Output:
    chargers_by_division.png  (300 DPI, ready for report/paper insertion)
    chargers_by_division.pdf  (vector version, ideal for LaTeX/Word figures)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------
INPUT_FILE = "Western_Province_EV_Chargers.xlsx"   # place file in same folder
DIVISION_COL = "Divisional Secretary's Division"
OUTPUT_PNG = "chargers_by_division.png"
OUTPUT_PDF = "chargers_by_division.pdf"

# Known inconsistent spellings in the raw dataset -> canonical name
NAME_FIXES = {
    "Negambo": "Negombo",
}

# ---------------------------------------------------------------------------
# 2. Load and clean data
# ---------------------------------------------------------------------------
df = pd.read_excel(INPUT_FILE, header=1)  # row 1 is the title, row 2 is the header

df[DIVISION_COL] = (
    df[DIVISION_COL]
    .astype(str)
    .str.strip()
    .replace(NAME_FIXES)
)

counts = (
    df[DIVISION_COL]
    .value_counts()
    .sort_values(ascending=True)   # ascending so largest bar ends up on top after barh
)

# ---------------------------------------------------------------------------
# 3. Plot styling (clean, print-ready, research-paper appropriate)
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
})

fig_height = max(6, len(counts) * 0.28)
fig, ax = plt.subplots(figsize=(8, fig_height), dpi=300)

bar_color = "#2E6F9E"      # muted professional blue
highlight_color = "#B33A3A"  # reserved for optional emphasis

bars = ax.barh(counts.index, counts.values, color=bar_color, height=0.65,
                edgecolor="white", linewidth=0.4, zorder=3)

# Value labels at the end of each bar
for bar, value in zip(bars, counts.values):
    ax.text(
        bar.get_width() + 0.15,
        bar.get_y() + bar.get_height() / 2,
        f"{int(value)}",
        va="center", ha="left", fontsize=9, color="#222222"
    )

# Axis formatting
ax.set_xlabel("Number of EV Charging Stations", fontsize=11, labelpad=8)
ax.set_ylabel("Divisional Secretary's Division", fontsize=11, labelpad=8)
ax.set_title(
    "Distribution of EV Charging Stations Across Divisional Secretary's\n"
    "Divisions, Western Province, Sri Lanka",
    fontsize=13, fontweight="bold", pad=14
)

ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.set_xlim(0, counts.max() * 1.12)

# Subtle gridlines behind bars, remove top/right spines
ax.grid(axis="x", linestyle="--", linewidth=0.5, color="#cccccc", zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

# Source / footnote for research context
fig.text(
    0.02, -0.01,
    "Source: John Keells CG Auto EV Charger Network dataset, Western Province, Sri Lanka.",
    fontsize=8, color="#555555", ha="left"
)

plt.tight_layout()

# ---------------------------------------------------------------------------
# 4. Save outputs
# ---------------------------------------------------------------------------
fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
fig.savefig(OUTPUT_PDF, bbox_inches="tight")

print(f"Saved: {OUTPUT_PNG}")
print(f"Saved: {OUTPUT_PDF}")
print("\nStation counts per division:")
print(counts.sort_values(ascending=False).to_string())
