import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1. Load Dataset
# ==============================
file_path = "C:/Users/DELL/Downloads/Western_Province_Data.xlsx"  
df = pd.read_excel(file_path)

# ==============================
# 2. Check Columns
# ==============================
print("Columns in Dataset:")
print(df.columns)

# Replace these names if your dataset has different column names
year_col = "Manufacture Year"
count_col = "Count"

# ==============================
# 3. Group Data by Year
# ==============================
yearly_ev = (
    df.groupby(year_col)[count_col]
      .sum()
      .reset_index()
      .sort_values(by=year_col)
)

# Remove missing years
yearly_ev = yearly_ev.dropna(subset=[year_col])

# Convert Manufacture Year to integer
yearly_ev[year_col] = yearly_ev[year_col].astype(int)

# ==============================
# 4. Calculate Growth Metrics
# ==============================
yearly_ev["Cumulative EVs"] = yearly_ev[count_col].cumsum()
yearly_ev["Growth Rate (%)"] = yearly_ev[count_col].pct_change() * 100

# ==============================
# 5. Summary Statistics
# ==============================
print("\n========== SUMMARY ==========")
print("Total EV Registrations :", yearly_ev[count_col].sum())
print("Average per Year       :", round(yearly_ev[count_col].mean(), 2))

print("\nHighest Registration:")
print(yearly_ev.loc[yearly_ev[count_col].idxmax()])

print("\nLowest Registration:")
print(yearly_ev.loc[yearly_ev[count_col].idxmin()])

# ==============================
# 6. Plot 1 - Line Chart
# ==============================
plt.figure(figsize=(12, 5))
plt.plot(
    yearly_ev[year_col],
    yearly_ev[count_col],
    marker='o',
    linewidth=2
)

plt.title("Year-wise EV Growth")
plt.xlabel("Manufacture Year")
plt.ylabel("Number of EV Registrations")
plt.xticks(yearly_ev[year_col])  # Integer years only
plt.grid(False)
plt.tight_layout()
plt.show()

# ==============================
# 7. Plot 2 - Bar Chart
# ==============================
plt.figure(figsize=(12, 5))
plt.bar(
    yearly_ev[year_col],
    yearly_ev[count_col]
)

plt.title("Year-wise EV Registrations")
plt.xlabel("Manufacture Year")
plt.ylabel("EV Count")
plt.xticks(yearly_ev[year_col])  # Integer years only
plt.tight_layout()
plt.show()

# ==============================
# 8. Plot 3 - Cumulative Growth
# ==============================
plt.figure(figsize=(12, 5))
plt.plot(
    yearly_ev[year_col],
    yearly_ev["Cumulative EVs"],
    marker='o',
    linewidth=2
)

plt.title("Cumulative EV Growth")
plt.xlabel("Manufacture Year")
plt.ylabel("Cumulative EV Count")
plt.xticks(yearly_ev[year_col])  # Integer years only
plt.grid(False)
plt.tight_layout()
plt.show()

# ==============================
# 9. Display Final Table
# ==============================
print("\n========== YEAR-WISE EV ANALYSIS ==========")
print(yearly_ev)

# ==============================
# 10. Save Results
# ==============================
output_file = "Yearwise_EV_Growth_Analysis.xlsx"
yearly_ev.to_excel(output_file, index=False)

print("\nAnalysis Completed Successfully!")
print("Results saved as:", output_file)
print("Results saved as:", output_file)
