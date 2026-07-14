import pandas as pd
import numpy as np

INPUT_PATH = r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\Merged_dataset.xlsx"
OUTPUT_PATH = r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx"


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
    df.columns = [str(col).strip() if pd.notna(col) else f"Unnamed_{i}" for i, col in enumerate(df.columns)]
    return df


# ===========================
# Load Data
# ===========================
input_df = load_dataset(INPUT_PATH)

district_col = find_column(input_df.columns, ["District", "district"])
ds_division_col = find_column(input_df.columns, ["Divisional Secretariat Division", "DS Division", "DS_Division", "Divisional Secretariat"])
population_col = find_column(input_df.columns, ["Population", "population"])
area_col = find_column(input_df.columns, ["Area", "area"])
district_ev_col = find_column(input_df.columns, ["District EV Count", "District_EV", "district ev count", "District EV"])

# ---------------------------------------------------------
# Drop notes/blank rows that aren't real DS records BEFORE
# any computation, so they can't pollute groupby results.
# ---------------------------------------------------------
input_df = input_df[
    input_df[district_col].notna()
    & input_df[population_col].notna()
    & input_df[ds_division_col].notna()
].reset_index(drop=True)

analysis_df = input_df[[district_col, ds_division_col, population_col, area_col, district_ev_col]].copy()
analysis_df.columns = ["District", "DS_Division", "Population", "Area", "District_EV"]

for col in ["Population", "Area", "District_EV"]:
    analysis_df[col] = pd.to_numeric(analysis_df[col], errors="coerce")

if analysis_df["Area"].isna().all():
    raise ValueError(
        "The 'Area' column is empty for every row. Density / Urbanization Score "
        "cannot be computed without real area values per DS division — fill this "
        "in before running the allocation."
    )

out_df = input_df.copy()

# ===========================
# Step 1: Population Share, Density, Urbanization Score
# (all computed WITHIN each district)
# ===========================
out_df["PopulationShare"] = (
    analysis_df["Population"] / analysis_df.groupby(analysis_df["District"])["Population"].transform("sum")
)

out_df["Density"] = analysis_df["Population"] / analysis_df["Area"]

out_df["UrbanizationScore"] = (
    out_df.groupby(district_col)["Density"]
    .transform(lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0)
)
out_df["UrbanizationScore"] = out_df["UrbanizationScore"].fillna(0)

# ===========================
# Step 2: District-wise Entropy Weighting on (PopulationShare, UrbanizationScore)
# — same two quantities that feed the demand score in Step 3, no extra
# normalization layer in between.
# ===========================
out_df["x"] = np.nan
out_df["y"] = np.nan

for district in analysis_df["District"].unique():
    idx = analysis_df["District"] == district
    criteria = out_df.loc[idx, ["PopulationShare", "UrbanizationScore"]].copy()
    criteria = criteria.replace(0, 1e-12)

    n = len(criteria)
    if n <= 1:
        x, y = 0.5, 0.5
    else:
        P = criteria / criteria.sum(axis=0)
        E = -(P * np.log(P)).sum(axis=0) / np.log(n)
        D = 1 - E
        weights = D / D.sum() if D.sum() != 0 else pd.Series([0.5, 0.5], index=criteria.columns)
        x = weights["PopulationShare"]
        y = weights["UrbanizationScore"]

    out_df.loc[idx, "x"] = x
    out_df.loc[idx, "y"] = y

    print(f"{district}")
    print(f"Population Weight (x): {x:.4f}")
    print(f"Urbanization Weight (y): {y:.4f}")
    print("-" * 40)

# ===========================
# Step 3: Demand Score
# ===========================
out_df["DemandScore"] = (
    out_df["x"] * out_df["PopulationShare"] + out_df["y"] * out_df["UrbanizationScore"]
)

# ===========================
# Step 4: Allocate District EVs
# ===========================
out_df["TotalScore"] = out_df.groupby(district_col)["DemandScore"].transform("sum")

out_df["Estimated_EV"] = np.where(
    out_df["TotalScore"] > 0,
    analysis_df["District_EV"] * out_df["DemandScore"] / out_df["TotalScore"],
    0,
)
out_df["Estimated_EV"] = out_df["Estimated_EV"].round()

# ===========================
# Rearrange & Save
# ===========================
new_columns = ["PopulationShare", "Density", "UrbanizationScore", "x", "y", "DemandScore", "TotalScore", "Estimated_EV"]
existing = list(input_df.columns)
new_columns = [col for col in new_columns if col in out_df.columns]
out_df = out_df[existing + new_columns]

out_df = out_df.loc[:, ~out_df.isna().all()]
out_df.to_excel(OUTPUT_PATH, index=False)

print("Completed Successfully")