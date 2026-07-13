import pandas as pd
from openpyxl import load_workbook


def clean_column_names(frame):
    frame = frame.copy()
    frame.columns = (
        frame.columns.astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    return frame


def resolve_column(frame, candidates, label):
    lookup = {column.casefold(): column for column in frame.columns}
    for candidate in candidates:
        resolved = lookup.get(candidate.casefold())
        if resolved is not None:
            return resolved
    raise ValueError(
        f"Could not find a {label} column. Available columns: {list(frame.columns)}"
    )


# -----------------------------------
# Read the datasets
# -----------------------------------
population_workbook = load_workbook(
    r"D:\LMS\3.1\Gruop Project\Population_Table_western.xlsx",
    data_only=True,
    read_only=True,
)
population_sheet = population_workbook.active

population_rows = []
current_district = None

for district, ds_division, *_ in population_sheet.iter_rows(min_row=8, values_only=True):
    if district is None and ds_division is None:
        continue

    if district is not None:
        district_text = str(district).strip()
        if district_text and district_text.lower() != "nan":
            current_district = district_text

    ds_text = "" if ds_division is None else str(ds_division).strip()
    if not ds_text or ds_text.lower() == "nan":
        continue

    population_rows.append(
        {
            "District": current_district,
            "DS Division": ds_text,
        }
    )

population = pd.DataFrame(population_rows)

chargers = pd.read_excel(
    r"D:\LMS\3.1\Gruop Project\Western_Province_EV_Chargers.xlsx",
    header=1,
)

# -----------------------------------
# Clean column names
# -----------------------------------
population = clean_column_names(population)
chargers = clean_column_names(chargers)

chargers.rename(
    columns={
        resolve_column(chargers, ["Divisional Secretary's Division", "DS Division"], "charger DS division"): "DS Division",
        resolve_column(chargers, ["District"], "charger district"): "District",
    },
    inplace=True,
)

population["District"] = population["District"].astype(str).str.strip()
population["DS Division"] = population["DS Division"].astype(str).str.strip()
chargers["District"] = chargers["District"].astype(str).str.strip()
chargers["DS Division"] = chargers["DS Division"].astype(str).str.strip()

population = population[
    population["District"].notna()
    & population["DS Division"].notna()
    & (population["District"].str.lower() != "nan")
    & (population["DS Division"].str.lower() != "nan")
]

chargers = chargers[
    chargers["District"].notna()
    & chargers["DS Division"].notna()
    & (chargers["District"].str.lower() != "nan")
    & (chargers["DS Division"].str.lower() != "nan")
]

# -----------------------------------
# Count charging stations by District
# and DS Division
# -----------------------------------
charger_count = (
    chargers.groupby(["District", "DS Division"])
    .size()
    .reset_index(name="Charging Stations")
)

# -----------------------------------
# Merge with population data
# -----------------------------------
merged = population.merge(
    charger_count,
    on=["District", "DS Division"],
    how="left"
)

# Replace missing values with 0
merged["Charging Stations"] = (
    merged["Charging Stations"]
    .fillna(0)
    .astype(int)
)

# -----------------------------------
# Save output
# -----------------------------------
output_file = r"D:\LMS\3.1\Gruop Project\DS_Population_Chargers.xlsx"

merged.to_excel(output_file, index=False)

print("Dataset merged successfully!")
print("Saved to:", output_file)