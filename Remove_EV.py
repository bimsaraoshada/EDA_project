import pandas as pd

# File path
file_path = r"D:/LMS/3.1/Gruop Project/EV_edited.xlsx"

# Read sheets
sheet1 = pd.read_excel(file_path, sheet_name="Sheet1", header=1)
sheet2 = pd.read_excel(file_path, sheet_name="Sheet2")

# Normalize column names so the script is resilient to extra spaces in headers
sheet1.columns = sheet1.columns.astype(str).str.strip()
sheet2.columns = sheet2.columns.astype(str).str.strip()

required_sheet1 = {"Make", "Model"}
required_sheet2 = {"Unique Make", "Model", "Status"}

missing_sheet1 = required_sheet1 - set(sheet1.columns)
missing_sheet2 = required_sheet2 - set(sheet2.columns)

if missing_sheet1:
    raise ValueError(f"Sheet1 is missing required columns: {sorted(missing_sheet1)}. Found: {sheet1.columns.tolist()}")

if missing_sheet2:
    raise ValueError(f"Sheet2 is missing required columns: {sorted(missing_sheet2)}. Found: {sheet2.columns.tolist()}")

# Clean text (ignore case and extra spaces)
sheet1["Make"] = sheet1["Make"].astype(str).str.strip().str.upper()
sheet1["Model"] = sheet1["Model"].astype(str).str.strip().str.upper()

sheet2["Unique Make"] = sheet2["Unique Make"].astype(str).str.strip().str.upper()
sheet2["Model"] = sheet2["Model"].astype(str).str.strip().str.upper()
sheet2["Status"] = sheet2["Status"].astype(str).str.strip().str.upper()

# Get all Non-EV (NEV) Make-Model pairs
nev_pairs = set(
    zip(
        sheet2.loc[sheet2["Status"] == "NEV", "Unique Make"],
        sheet2.loc[sheet2["Status"] == "NEV", "Model"]
    )
)

# Remove Non-EV records from Sheet1
cleaned_sheet1 = sheet1[
    ~sheet1.apply(
        lambda row: (row["Make"], row["Model"]) in nev_pairs,
        axis=1
    )
]

# Save cleaned dataset
output_file = r"D:/LMS/3.1/Gruop Project/EV_Cleaned.xlsx"
cleaned_sheet1.to_excel(output_file, index=False)

print("Non-EV vehicles removed successfully!")
print(f"Original rows: {len(sheet1)}")
print(f"Remaining rows: {len(cleaned_sheet1)}")
print(f"Rows removed: {len(sheet1) - len(cleaned_sheet1)}")