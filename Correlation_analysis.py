import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx")

# Check columns
df.columns

# Calculate correlation population vs estimated EV demand
r_population = df["Population"].corr(df["Estimated_EV"])

print("Correlation (Population vs EV Demand):", round(r_population,3))


# Scatter plot
plt.figure(figsize=(8,5))

plt.scatter(
    df["Population"],
    df["Estimated_EV"]
)

plt.xlabel("Population")
plt.ylabel("Estimated EV Demand")
plt.title(
    f"Population vs Estimated EV Demand (r = {r_population:.3f})"
)

plt.grid(True)
plt.show()

# Calculate correlation urbanization score vs estimated EV demand
r_urban = df["UrbanizationScore"].corr(
    df["Estimated_EV"]
)

print(
    "Correlation (Urbanization Score vs EV Demand):",
    round(r_urban,3)
)


# Scatter plot
plt.figure(figsize=(8,5))

plt.scatter(
    df["UrbanizationScore"],
    df["Estimated_EV"]
)

plt.xlabel("Urbanization Score")
plt.ylabel("Estimated EV Demand")

plt.title(
    f"Urbanization Score vs Estimated EV Demand (r = {r_urban:.3f})"
)

plt.grid(True)
plt.show()

# Calculate correlation demand score vs estimated EV demand
r_demand = df["DemandScore"].corr(
    df["Estimated_EV"]
)

print(
    "Correlation (Demand Score vs EV Demand):",
    round(r_demand,3)
)


# Scatter plot
plt.figure(figsize=(8,5))

plt.scatter(
    df["DemandScore"],
    df["Estimated_EV"]
)

plt.xlabel("Demand Score")
plt.ylabel("Estimated EV Demand")

plt.title(
    f"Demand Score vs Estimated EV Demand (r = {r_demand:.3f})"
)

plt.grid(True)
plt.show()

#correlation matrix and heatmap
corr_columns = [
    "Population",
    "PopulationShare",
    "UrbanizationScore",
    "DemandScore",
    "Estimated_EV"
]


corr_matrix = df[corr_columns].corr()


print(corr_matrix)

plt.figure(figsize=(8,6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Matrix of EV Demand Factors")

plt.show()