import pandas as pd

# Load the dataset
df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx")

# -----------------------------
# 1. Dataset Overview
# -----------------------------
print("="*50)
print("DATASET OVERVIEW")
print("="*50)

# Number of observations and variables
print(f"Number of observations (rows): {df.shape[0]}")
print(f"Number of variables (columns): {df.shape[1]}")

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Select numerical columns
numerical_columns = [
    'Population',
    'PopulationShare',
    'UrbanizationScore',
    'DemandScore',
    'Estimated_EV'
]

# Descriptive statistics
descriptive_stats = pd.DataFrame({
    'Mean': df[numerical_columns].mean(),
    'Median': df[numerical_columns].median(),
    'Std Dev': df[numerical_columns].std(),
    'Min': df[numerical_columns].min(),
    'Max': df[numerical_columns].max()
})

print("\nDescriptive Statistics")
print(descriptive_stats.round(3))