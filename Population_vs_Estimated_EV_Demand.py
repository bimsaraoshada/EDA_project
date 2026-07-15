import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel("C:/Users/DELL/Downloads/EV_Demand_Output.xlsx")

# Scatter plot
plt.figure(figsize=(8,6))
plt.scatter(df["Population"], df["Estimated_EV"])

plt.title("Population vs Estimated EV Demand")
plt.xlabel("Population")
plt.ylabel("Estimated EV Demand")

plt.grid(True)
plt.tight_layout()
plt.show()