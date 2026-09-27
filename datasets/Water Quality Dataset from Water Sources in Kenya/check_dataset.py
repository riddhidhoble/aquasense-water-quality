import pandas as pd
import os

file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "water_quality_dataset1.csv"
)

df = pd.read_csv(file_path)

print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())
print("\nLabel Distribution:")
print(df["Label"].value_counts())

print("\nLabel Percentage:")
print(df["Label"].value_counts(normalize=True) * 100)
print("\nParameter Statistics:")
print(df[["pH", "TDS_ppm", "Turbidity_NTU", "Temperature_C"]].describe())