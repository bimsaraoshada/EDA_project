import pandas as pd

# ---------------------------------
# 1. Load Raw Dataset
# ---------------------------------

file_path = r"c:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\Ev_vehicles_tilldec2025.xlsx"

# Use the second row as column headers (skip title row)
df = pd.read_excel(file_path, header=1)

# Remove any unwanted Unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print("=" * 50)
print("RAW DATASET LOADED")
print("=" * 50)

print(f"Number of observations (rows): {df.shape[0]}")
print(f"Number of variables (columns): {df.shape[1]}")


# ---------------------------------
# 2. Dataset Overview
# ---------------------------------

print("\n" + "=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)


# Show column names
print("\nColumn Names:")
print(df.columns.tolist())


# Show data types
print("\nData Types:")
print(df.dtypes)


# Show first 5 rows
print("\nFirst 5 Records:")
print(df.head())


# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Check duplicate rows
print("\nDuplicate Rows:")
print(f"Total duplicate rows: {df.duplicated().sum()}")


# Check unique values
print("\nUnique Values:")
for column in df.columns:
    print(f"{column}: {df[column].nunique()}")