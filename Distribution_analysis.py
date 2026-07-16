import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx")
columns = ["Population", "Estimated_EV", "DemandScore"]

for col in columns:
    data = df[col].dropna()

    # Histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(data, bins=15, color="#4C72B0", edgecolor="white")
    plt.title(f"Histogram of {col}", fontsize=13, fontweight="bold")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    # KDE
    plt.figure(figsize=(8, 5))
    sns.kdeplot(data, fill=True, color="#55A868")
    plt.title(f"KDE of {col}", fontsize=13, fontweight="bold")
    plt.xlabel(col)
    plt.ylabel("Density")
    plt.tight_layout()
    plt.show()

    print("="*60)
    print(f"{col}")
    print("="*60)
    print(f"Mean      : {data.mean():.2f}")
    print(f"Median    : {data.median():.2f}")
    print(f"Skewness  : {data.skew():.3f}")
    print(f"Kurtosis  : {data.kurt():.3f}")
    print()