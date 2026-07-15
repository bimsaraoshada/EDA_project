import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\Western_Province_Data.xlsx")

# Replace these with your actual column names
year_col = "Manufacture Year"
district_col = "District"

# If each row is one registered EV
yearly = (
    df.groupby([year_col, district_col])
      .size()
      .unstack(fill_value=0)
      .sort_index()
)

# If your dataset has a Count column instead, use:
# yearly = (
#     df.groupby([year_col, district_col])['Count']
#       .sum()
#       .unstack(fill_value=0)
#       .sort_index()
# )

print(yearly)

# -----------------------------
# Cumulative Demand
# -----------------------------
cumulative = yearly.cumsum()

plt.figure(figsize=(10,6))

for district in cumulative.columns:
    plt.plot(cumulative.index, cumulative[district],
             marker='o', linewidth=2, label=district)

plt.title("Cumulative Registered EVs")
plt.xlabel("Registration Year")
plt.ylabel("Cumulative EV Registrations")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# District Share (%)
# -----------------------------
share = yearly.div(yearly.sum(axis=1), axis=0) * 100

plt.figure(figsize=(10,6))

plt.stackplot(
    share.index,
    *[share[col] for col in share.columns],
    labels=share.columns
)

plt.title("District Share of EV Registrations")
plt.xlabel("Registration Year")
plt.ylabel("Share (%)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()


# -----------------------------
# Annual Demand Growth Rate (%)
# -----------------------------
demand_rate = yearly.pct_change() * 100

# Remove first year (NaN)
demand_rate = demand_rate.dropna()

plt.figure(figsize=(10,6))

for district in demand_rate.columns:
    plt.plot(
        demand_rate.index,
        demand_rate[district],
        marker='o',
        linewidth=2,
        label=district
    )

plt.title("Annual EV Demand Growth Rate by District")
plt.xlabel("Registration Year")
plt.ylabel("Demand Rate (%)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# Save to Excel if needed
demand_rate.to_excel("District_Demand_Growth_Rate.xlsx")