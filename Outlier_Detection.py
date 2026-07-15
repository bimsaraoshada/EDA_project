import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel("C:/Users/DELL/Downloads/EV_Demand_Output.xlsx")

# Variables to check
variables = [
    "Population",
    "DemandScore",
    "Estimated_EV"
]

# Outlier detection and boxplots
for variable in variables:

    # Calculate IQR
    Q1 = df[variable].quantile(0.25)
    Q3 = df[variable].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers
    outliers = df[
        (df[variable] < lower_bound) |
        (df[variable] > upper_bound)
    ]

    # Print results
    print("\n" + "=" * 60)
    print(f"Outlier Analysis for {variable}")
    print("=" * 60)
    print(f"Number of outliers: {len(outliers)}")

    if len(outliers) > 0:
        print(outliers[["District",
                        "Divisional Secretariat Division",
                        variable]])
    else:
        print("No outliers found.")

# Create one boxplot for each variable
for variable in variables:

    plt.figure(figsize=(6,5))

    plt.boxplot(df[variable])

    plt.title(f"Boxplot of {variable}")
    plt.ylabel(variable)

    plt.tight_layout()
    plt.show()