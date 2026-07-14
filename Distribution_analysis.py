import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx")

# Columns to analyze
columns = [
    "Population",
    "Estimated_EV",
    "DemandScore"
]

for col in columns:

    plt.figure(figsize=(8,5))
    plt.hist(df[col], bins=10)
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    print("="*60)
    print(f"{col}")
    print("="*60)
    print(f"Mean      : {df[col].mean():.2f}")
    print(f"Median    : {df[col].median():.2f}")
    print(f"Skewness  : {df[col].skew():.3f}")
    print(f"Kurtosis  : {df[col].kurt():.3f}")
    print()