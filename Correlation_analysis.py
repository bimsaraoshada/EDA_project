import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel("C:/Users/DELL/Downloads/EV_Demand_Output.xlsx")

# Select variables for correlation
correlation = df[
    [
        "Population",
        "PopulationShare",
        "UrbanizationScore",
        "DemandScore",
        "Estimated_EV"
    ]
].corr()

# Print correlation matrix
print("Correlation Matrix:\n")
print(correlation)

# Plot heatmap
plt.figure(figsize=(8,6))

plt.imshow(correlation, cmap="coolwarm", interpolation="nearest")
plt.colorbar()

plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45)
plt.yticks(range(len(correlation.columns)), correlation.columns)

plt.title("Correlation Heatmap")

# Display correlation values
for i in range(len(correlation.columns)):
    for j in range(len(correlation.columns)):
        plt.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center",
            color="black"
        )

plt.tight_layout()
plt.show()
plt.show()
