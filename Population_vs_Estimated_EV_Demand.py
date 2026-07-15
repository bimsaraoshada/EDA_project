import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel("C:/Users/DELL/Downloads/EV_Demand_Output.xlsx")

# Scatter plot
plt.figure(figsize=(13, 15))
plt.scatter(df["Population"], df["Estimated_EV"])

# Add labels to each point
for i, row in df.iterrows():
    plt.annotate(
        row["Divisional Secretariat Division"],
        (row["Population"], row["Estimated_EV"]),
        fontsize=8,
        xytext=(5,5),
        textcoords="offset points"
    )

plt.title("Population vs Estimated EV Demand")
plt.xlabel("Population")
plt.ylabel("Estimated EV Demand")

plt.grid(True)
plt.tight_layout()
plt.show()
