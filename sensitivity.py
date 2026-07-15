# ==========================================================
# SENSITIVITY ANALYSIS OF EV ALLOCATION
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# File Paths
# -----------------------------

INPUT_PATH = r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx"

OUTPUT_PATH = r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Sensitivity_Output.xlsx"


# -----------------------------
# Read Input File
# -----------------------------

df = pd.read_excel(INPUT_PATH)


# -----------------------------
# Select Required Columns
# -----------------------------

sensitivity_df = df[
    [
        "District",
        "Divisional Secretariat Division",
        "PopulationShare",
        "UrbanizationScore",
        "District EV Count",
        "Estimated_EV"
    ]
].copy()


# Rename entropy-based allocation

sensitivity_df.rename(
    columns={
        "Estimated_EV": "Entropy",
        "Divisional Secretariat Division": "DS_Division"
    },
    inplace=True
)


print(sensitivity_df.head())


# -----------------------------
# Define Sensitivity Scenarios
# -----------------------------

scenarios = {

    "30_70": (0.30,0.70),
    "40_60": (0.40,0.60),
    "50_50": (0.50,0.50),
    "60_40": (0.60,0.40),
    "70_30": (0.70,0.30)

}


# -----------------------------
# Sensitivity Calculations
# -----------------------------

for scenario,(population_weight,urban_weight) in scenarios.items():


    demand = (

        population_weight *
        sensitivity_df["PopulationShare"]

        +

        urban_weight *
        sensitivity_df["UrbanizationScore"]

    )


    # District total demand

    total_demand = demand.groupby(
        sensitivity_df["District"]
    ).transform("sum")


    # Allocate EVs

    ev_allocation = np.where(

        total_demand > 0,

        sensitivity_df["District EV Count"]
        *
        demand
        /
        total_demand,

        0

    )


    sensitivity_df[scenario] = np.round(
        ev_allocation
    ).astype(int)


    # Difference from entropy method

    sensitivity_df[f"Diff_{scenario}"] = (

        sensitivity_df[scenario]
        -
        sensitivity_df["Entropy"]

    )


print("Sensitivity Analysis Completed")

# -----------------------------
# Grouped Bar Chart
# -----------------------------

plot_df = sensitivity_df.set_index(
    "DS_Division"
)


plot_columns = [

    "Entropy",
    "30_70",
    "40_60",
    "50_50",
    "60_40",
    "70_30"

]


plot_df[plot_columns].plot(

    kind="bar",

    figsize=(20,8)

)


plt.ylabel(
    "Estimated EV Count"
)

plt.xlabel(
    "DS Division"
)

plt.title(
    "Sensitivity Analysis of Estimated EV Allocation"
)


plt.tight_layout()


plt.savefig(
    "Sensitivity_BarChart.png",
    dpi=300
)


plt.close()



# -----------------------------
# Scatter Plot
# -----------------------------

plt.figure(
    figsize=(7,7)
)


plt.scatter(

    sensitivity_df["Entropy"],

    sensitivity_df["60_40"]

)


maximum = max(

    sensitivity_df["Entropy"].max(),

    sensitivity_df["60_40"].max()

)


plt.plot(

    [0,maximum],

    [0,maximum],

    "r--"

)


plt.xlabel(
    "Entropy Weight Allocation"
)


plt.ylabel(
    "60:40 Allocation"
)


plt.title(
    "Entropy vs 60:40 Allocation"
)


plt.tight_layout()


plt.savefig(

    "Scatter_Entropy_vs_60_40.png",

    dpi=300

)


plt.close()



# -----------------------------
# Sensitivity Summary
# -----------------------------

summary = []


for scenario in scenarios.keys():


    diff = sensitivity_df[
        f"Diff_{scenario}"
    ]


    summary.append({

        "Scenario": scenario,

        "Mean Difference": diff.mean(),

        "Mean Absolute Difference":
            diff.abs().mean(),

        "Maximum Difference":
            diff.abs().max(),

        "Changed DS Divisions":
            (diff != 0).sum()

    })


summary_df = pd.DataFrame(summary)


print(summary_df)



# -----------------------------
# Save Excel Output
# -----------------------------

with pd.ExcelWriter(

    OUTPUT_PATH,

    engine="openpyxl"

) as writer:


    sensitivity_df.to_excel(

        writer,

        sheet_name="Sensitivity Analysis",

        index=False

    )


    summary_df.to_excel(

        writer,

        sheet_name="Summary",

        index=False

    )



print("Excel Saved Successfully")
print(OUTPUT_PATH)