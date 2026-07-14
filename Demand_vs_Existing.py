import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Load dataset
df = pd.read_excel(r"C:\Users\ASUS\OneDrive\LMS\3.1\Gruop Project\EV_Demand_Output.xlsx")

# Convert numeric columns
df["Estimated_EV"] = pd.to_numeric(df["Estimated_EV"], errors="coerce")
df["Existing Charging Points in Divisional Secretariat"] = pd.to_numeric(
    df["Existing Charging Points in Divisional Secretariat"],
    errors="coerce"
)

df = df.dropna()


plt.figure(figsize=(14,10))

plt.scatter(
    df["Estimated_EV"],
    df["Existing Charging Points in Divisional Secretariat"],
    s=70,
    alpha=0.6
)

texts = []

for i in range(len(df)):
    texts.append(
        plt.text(
            df["Estimated_EV"].iloc[i],
            df["Existing Charging Points in Divisional Secretariat"].iloc[i],
            df["Divisional Secretariat Division"].iloc[i],
            fontsize=7
        )
    )

# Faster adjustment
adjust_text(
    texts,
    only_move={'points':'y', 'texts':'y'},
    arrowprops=dict(
        arrowstyle="-",
        lw=0.4
    ),
    time_lim=2
)

plt.title("Estimated EV Demand vs Existing Charging Points")
plt.xlabel("Estimated EV Demand")
plt.ylabel("Existing Charging Points")
plt.grid(True)

plt.tight_layout()
plt.show()