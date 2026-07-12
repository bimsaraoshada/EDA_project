import pandas as pd
import os

# File path
file_path = r"D:\LMS\3.1\Gruop Project\EV_Cleaned.xlsx"

# Read the Excel file
df = pd.read_excel(file_path)

# -------------------------------
# Remove exact duplicate rows
# -------------------------------
duplicate_rows = df[df.duplicated()]
removed_row_numbers = (duplicate_rows.index + 2).tolist()

df = df.drop_duplicates()

print("Exact duplicate removal completed!")
print(f"Duplicate rows removed: {len(removed_row_numbers)}")

if removed_row_numbers:
    print(f"Removed Excel row numbers: {removed_row_numbers}")
else:
    print("No duplicate rows found.")

# -------------------------------
# Merge rows and sum Count
# -------------------------------
before_grouping = len(df)

df = df.groupby(
    ["Vehicle Category", "Make", "Model", "Manufacture Year", "District"],
    as_index=False
)["Count"].sum()

after_grouping = len(df)

print(f"Rows merged by grouping: {before_grouping - after_grouping}")

# -------------------------------
# Save the cleaned dataset
# -------------------------------
output_file = r"D:\LMS\3.1\Gruop Project\EV_No_Duplicates.xlsx"
df.to_excel(output_file, index=False)

print(f"Cleaned Excel file saved as: {os.path.basename(output_file)}")