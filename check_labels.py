import pandas as pd
import os

# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

base_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    base_path,
    "datasets",
    "Water Quality Dataset from Water Sources in Kenya",
    "water_quality_dataset1.csv"
)

df = pd.read_csv(file_path)

# --------------------------------------------------
# 2. Calculate Statistics for Each Class
# --------------------------------------------------

parameters = [
    "pH",
    "TDS_ppm",
    "Turbidity_NTU",
    "Temperature_C"
]

print("Safe vs Unsafe Parameter Statistics")
print("=" * 60)

for parameter in parameters:

    print(f"\n{parameter}")

    statistics = df.groupby("Label")[parameter].agg(
        ["min", "mean", "max"]
    )

    print(statistics)

# --------------------------------------------------
# 3. Check Class Counts
# --------------------------------------------------

print("\n\nClass Counts")
print("=" * 60)

print(df["Label"].value_counts())