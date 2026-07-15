import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_excel("C:/Users/DELL/Downloads/EV_Demand_Output.xlsx")

# ======================================================
# District-wise EV Demand
# ======================================================

district_growth = (
    df.groupby("District")["District EV Count"]
      .first()
      .sort_values(ascending=True)
)

plt.figure(figsize=(10, 6))
district_growth.plot(kind="barh")

plt.title("District-wise EV Demand")
plt.xlabel("EV Count")
plt.ylabel("District")

plt.tight_layout()
plt.show()

# ======================================================
# Divisional Secretariat-wise EV Demand
# ======================================================

ds_growth = (
    df.groupby("Divisional Secretariat Division")["Estimated_EV"]
      .sum()
      .sort_values(ascending=True)
)

plt.figure(figsize=(14, 18))
ds_growth.plot(kind="barh")

plt.title("Divisional Secretariat-wise EV Demand")
plt.xlabel("Estimated EV")
plt.ylabel("Divisional Secretariat Division")

plt.tight_layout()
plt.show()
plt.show()
