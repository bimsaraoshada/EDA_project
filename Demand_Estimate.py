import pandas as pd
import numpy as np

# ===========================
# Load Data
# ===========================
df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\Merged_dataset.xlsx")

# Columns required:
# District
# DS_Division
# Population
# Area
# District_EV

# ===========================
# Step 1: Population Share
# ===========================

df["PopulationShare"] = (
    df["Population"] /
    df.groupby("District")["Population"].transform("sum")
)

# ===========================
# Step 2: Population Density
# ===========================

df["Density"] = df["Population"] / df["Area"]

# ===========================
# Step 3: Urbanization Score
# Normalize Density within each district
# ===========================

df["UrbanizationScore"] = (
    df.groupby("District")["Density"]
      .transform(lambda x: (x-x.min())/(x.max()-x.min()))
)

# Replace NaN if only one DS exists in a district
df["UrbanizationScore"] = df["UrbanizationScore"].fillna(0)

# ===========================
# Step 4: Entropy Weight Method
# ===========================

criteria = df[["PopulationShare","UrbanizationScore"]].copy()

# Small value to avoid log(0)
criteria = criteria.replace(0,1e-12)

# Normalize columns
P = criteria / criteria.sum(axis=0)

n = len(criteria)

# Entropy
E = -(P*np.log(P)).sum(axis=0)/np.log(n)

# Degree of Diversification
D = 1-E

# Final weights
weights = D/D.sum()

x = weights["PopulationShare"]
y = weights["UrbanizationScore"]

print("Population Weight (x):", round(x,4))
print("Urbanization Weight (y):", round(y,4))

# ===========================
# Step 5: Demand Score
# ===========================

df["DemandScore"] = (
    x*df["PopulationShare"] +
    y*df["UrbanizationScore"]
)

# ===========================
# Step 6: Allocate District EVs
# ===========================

df["TotalScore"] = (
    df.groupby("District")["DemandScore"]
      .transform("sum")
)

df["Estimated_EV"] = (
    df["District_EV"] *
    df["DemandScore"] /
    df["TotalScore"]
)

# ===========================
# Save
# ===========================

df.to_excel("EV_Demand_Output.xlsx",index=False)

print("Completed Successfully")