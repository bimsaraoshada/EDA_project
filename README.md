# Electric Vehicle (EV) Dataset - Exploratory Data Analysis (EDA)

## Project Overview

This project focuses on data preprocessing and Exploratory Data Analysis (EDA) of an Electric Vehicle (EV) registration dataset. The aim is to improve the quality of the dataset by removing duplicate records, handling missing values, filtering unnecessary records, and generating province-specific datasets for further analysis.

## Team Members

- Bimsara Pallewaththa
- Yasanga03
- Kaushal Senevirathna

---

## Project Structure

```
EDA_project/
│
├── Duplicate.py                   # Removes duplicate records
├── Handle_Missing_Values.py       # Handles missing values
├── Remove_EV.py                   # Removes unnecessary EV records
├── project.py                     # Generates Western Province dataset
│
├── EV_edited.xlsx                 # Original dataset
├── EV_Cleaned.xlsx                # Cleaned dataset
├── EV_No_Duplicates.xlsx          # Dataset after duplicate removal
├── EV_Handled_Missing_Values.xlsx # Dataset after handling missing values
├── Western_Province_Data.xlsx     # Filtered Western Province dataset
│
└── README.md
```

---

## Dataset Processing Workflow

```
EV_edited.xlsx
        │
        ▼
EV_Cleaned.xlsx
        │
        ▼
EV_No_Duplicates.xlsx
        │
        ▼
EV_Handled_Missing_Values.xlsx
        │
        ▼
Western_Province_Data.xlsx
```

---

## Features

- Remove duplicate records from the dataset.
- Handle missing values using appropriate preprocessing techniques.
- Remove unnecessary EV records.
- Generate province-specific datasets.
- Export processed datasets in Excel (`.xlsx`) format.
- Perform efficient data preprocessing using the Pandas library.

---

## Technologies Used

- Python 3.x
- Pandas
- OpenPyXL
- Git
- GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/bimsaraoshada/EDA_project.git
```

Navigate to the project directory:

```bash
cd EDA_project
```

Install the required Python libraries:

```bash
pip install pandas openpyxl
```

---

## How to Run

Run the scripts in the following order:

```bash
python Duplicate.py
```

```bash
python Handle_Missing_Values.py
```

```bash
python Remove_EV.py
```

```bash
python project.py
```

---

## Input and Output Files

### Input

- `EV_edited.xlsx`

### Intermediate Files

- `EV_Cleaned.xlsx`
- `EV_No_Duplicates.xlsx`
- `EV_Handled_Missing_Values.xlsx`

### Output

- `Western_Province_Data.xlsx`

---

## Project Objectives

- Improve data quality by cleaning the EV dataset.
- Remove duplicate records.
- Handle missing values effectively.
- Remove unnecessary records.
- Generate province-wise datasets.
- Prepare the dataset for Exploratory Data Analysis (EDA).

---

## Future Improvements

- Generate datasets for all provinces automatically.
- Add visualizations using Matplotlib or Seaborn.
- Generate descriptive statistical reports.
- Build an interactive dashboard using Streamlit or Power BI.

---

## License

This project was developed for academic purposes as part of an **Exploratory Data Analysis (EDA)** group project.
