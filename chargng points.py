import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel dataset
file_path = r"C:\Users\User\Desktop\Group Project\Western_Province_Data_with_Charging_Port.xlsx"
df = pd.read_excel(file_path)

# Inspect column names to find the charging port column
print("Columns in the dataset:")
print(df.columns.tolist())

# Identify the charging port column
charging_port_column = "Fast Charger Port"

# Clean the charging port data
# 1) Remove missing values
# 2) Trim leading/trailing spaces
# 3) Convert text to uppercase
charging_port_series = df[charging_port_column].dropna().astype(str).str.strip().str.upper()
charging_port_series = charging_port_series[charging_port_series != ""]

# Print the frequency table before plotting
print("\nFrequency of charging port types:")
print(charging_port_series.value_counts())

# Count the frequency of each charging port type
port_counts = charging_port_series.value_counts()

# Create a pie chart
plt.figure(figsize=(10, 8))
colors = plt.cm.Set3(range(len(port_counts)))

wedges, texts, autotexts = plt.pie(
    port_counts,
    labels=port_counts.index,
    autopct="%.1f%%",
    startangle=90,
    explode=[0.05] * len(port_counts),
    shadow=True,
    colors=colors,
    pctdistance=0.6,
    textprops={"fontsize": 12, "color": "black"},
    wedgeprops={"edgecolor": "white", "linewidth": 1.2},
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontweight("bold")
    autotext.set_fontsize(12)

# Add title and keep chart circular
plt.title(
    "Distribution of EV Charging Port Types in the Western Province",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.axis("equal")
plt.tight_layout()

# Show the plot
plt.show()