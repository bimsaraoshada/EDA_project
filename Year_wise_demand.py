import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1. Load Dataset
# ==============================
file_path = r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\Western_Province_Data.xlsx"   # Change path if needed
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

# Remove missing years (if any)
yearly_ev = yearly_ev.dropna()

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
print("Average per Year       :", round(yearly_ev[count_col].mean(),2))
print("Highest Registration   :")
print(yearly_ev.loc[yearly_ev[count_col].idxmax()])
print("\nLowest Registration    :")
print(yearly_ev.loc[yearly_ev[count_col].idxmin()])

# ==============================
# 6. Plot 1 - Line Chart
# ==============================
plt.figure(figsize=(8,5))
plt.plot(yearly_ev[year_col], yearly_ev[count_col], marker='o', linewidth=2)
plt.title("Year-wise EV Growth")
plt.xlabel("Manufacture Year")
plt.ylabel("Number of EV Registrations")
plt.grid(True)
plt.tight_layout()
plt.show()

# ==============================
# 7. Plot 2 - Bar Chart
# ==============================
plt.figure(figsize=(8,5))
plt.bar(yearly_ev[year_col], yearly_ev[count_col])
plt.title("Year-wise EV Registrations")
plt.xlabel("Manufacture Year")
plt.ylabel("EV Count")
plt.tight_layout()
plt.show()

# ==============================
# 8. Plot 3 - Cumulative Growth
# ==============================
plt.figure(figsize=(8,5))
plt.plot(yearly_ev[year_col], yearly_ev["Cumulative EVs"], marker='o', linewidth=2)
plt.title("Cumulative EV Growth")
plt.xlabel("Manufacture Year")
plt.ylabel("Cumulative EV Count")
plt.grid(True)
plt.tight_layout()
plt.show()

# ==============================
# 9. Plot 4 - Growth Rate
# ==============================
plt.figure(figsize=(8,5))
plt.bar(yearly_ev[year_col], yearly_ev["Growth Rate (%)"])
plt.title("Annual EV Growth Rate (%)")
plt.xlabel("Manufacture Year")
plt.ylabel("Growth Rate (%)")
plt.tight_layout()
plt.show()

# ==============================
# 10. Save Results
# ==============================
output_file = "Yearwise_EV_Growth_Analysis.xlsx"
yearly_ev.to_excel(output_file, index=False)

print("\nAnalysis Completed Successfully!")
print("Results saved as:", output_file)