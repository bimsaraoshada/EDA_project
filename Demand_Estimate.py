import pandas as pd
import numpy as np

INPUT_PATH = "C:/Users/DELL/Downloads/Merged_dataset.xlsx"
OUTPUT_PATH = "C:/Users/DELL/Downloads/EV_Demand_Output.xlsx"


def normalize_column_name(name):
    if pd.isna(name):
        return ""
    return str(name).strip().lower()


def find_column(columns, candidates):
    normalized_columns = {normalize_column_name(col): col for col in columns}

    for candidate in candidates:
        if normalize_column_name(candidate) in normalized_columns:
            return normalized_columns[normalize_column_name(candidate)]

    for col in columns:
        normalized_col = normalize_column_name(col)
        for candidate in candidates:
            candidate_normalized = normalize_column_name(candidate)
            if candidate_normalized.replace(" ", "") in normalized_col.replace(" ", ""):
                return col

    raise KeyError(f"Could not find any of the expected columns: {candidates}")


def load_dataset(path):
    excel_file = pd.ExcelFile(path)
    sheet_name = "Merged Data" if "Merged Data" in excel_file.sheet_names else excel_file.sheet_names[0]

    raw_df = pd.read_excel(path, sheet_name=sheet_name, header=None)

    header_row = None
    for idx, row in raw_df.iterrows():
        values = [str(v).strip() if pd.notna(v) else "" for v in row.tolist()]
        if any("district" in value.lower() for value in values) and any("population" in value.lower() for value in values):
            header_row = idx
            break

    if header_row is None:
        header_row = 4

    df = pd.read_excel(path, sheet_name=sheet_name, header=header_row)

    df.columns = [
        str(col).strip() if pd.notna(col) else f"Unnamed_{i}"
        for i, col in enumerate(df.columns)
    ]
    return df


# ===========================
# Load Data
# ===========================
input_df = load_dataset(INPUT_PATH)

# Columns required:
# District
# DS_Division
# Population
# Area
# District_EV

district_col = find_column(input_df.columns, ["District", "district"])
ds_division_col = find_column(input_df.columns, ["Divisional Secretariat Division", "DS Division", "DS_Division", "Divisional Secretariat"])
population_col = find_column(input_df.columns, ["Population", "population"])
area_col = find_column(input_df.columns, ["Area", "area"])
district_ev_col = find_column(input_df.columns, ["District EV Count", "District_EV", "district ev count", "District EV"])

# Work on a standardized copy for the calculations while preserving the original input columns in the export.
analysis_df = input_df[[district_col, ds_division_col, population_col, area_col, district_ev_col]].copy()
analysis_df.columns = ["District", "DS_Division", "Population", "Area", "District_EV"]

# Convert numeric fields
for col in ["Population", "Area", "District_EV"]:
    analysis_df[col] = pd.to_numeric(analysis_df[col], errors="coerce")

# Keep all input columns in the final output and add the computed columns to them.
out_df = input_df.copy()

# Preserve the original input column names for shared columns by using the original dataframe.
# The computed values will be appended below.

# ===========================
# Step 1: Population Share
# ===========================

out_df["PopulationShare"] = (
    analysis_df["Population"] /
    analysis_df.groupby("District")["Population"].transform("sum")
)

# ===========================
# Step 2: Population Density
# ===========================

out_df["Density"] = analysis_df["Population"] / analysis_df["Area"]

# ===========================
# Step 3: Urbanization Score
# Normalize Density within each district
# ===========================

out_df["UrbanizationScore"] = (
    out_df.groupby("District")["Density"]
      .transform(lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0)
)

# Replace NaN if only one DS exists in a district
out_df["UrbanizationScore"] = out_df["UrbanizationScore"].fillna(0)

# ===========================
# Step 4: Entropy Weight Method
# ===========================

criteria = out_df[["PopulationShare", "UrbanizationScore"]].copy()

# Small value to avoid log(0)
criteria = criteria.replace(0, 1e-12)

# Normalize columns
P = criteria / criteria.sum(axis=0)

n = len(criteria)

# Entropy
E = -(P * np.log(P)).sum(axis=0) / np.log(n)

# Degree of Diversification
D = 1 - E

# Final weights
weights = D / D.sum()

x = float(weights.get("PopulationShare", 0.0))
y = float(weights.get("UrbanizationScore", 0.0))

print("Population Weight (x):", round(x, 4))
print("Urbanization Weight (y):", round(y, 4))

# ===========================
# Step 5: Demand Score
# ===========================

out_df["DemandScore"] = (
    x * out_df["PopulationShare"] +
    y * out_df["UrbanizationScore"]
)

# ===========================
# Step 6: Allocate District EVs
# ===========================

out_df["Estimated_EV"] = np.where(
    out_df["DemandScore"] > 0,
    analysis_df["District_EV"] * out_df["DemandScore"],
    0
)

# ===========================
# Save
# ===========================

# Remove columns that are entirely empty
out_df = out_df.loc[:, ~out_df.isna().all()]

out_df.to_excel(OUTPUT_PATH, index=False)

print("Completed Successfully")
