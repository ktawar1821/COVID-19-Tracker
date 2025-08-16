import pandas as pd
import numpy as np

# 1) Load
df = pd.read_csv("covid19_medium_dataset.csv", parse_dates=["Date"])

print("Shape:", df.shape)
print(df.head(), "\n")
print(df.info(), "\n")
print("Missing values:\n", df.isna().sum(), "\n")

# 2) Basic sanity checks
num_cols = ["Confirmed","Deaths","Recovered","Active","Tests Conducted"]
# drop negatives if any (shouldn’t exist, but be safe)
df = df[(df[num_cols] >= 0).all(axis=1)]

# remove exact duplicates
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# 3) Feature engineering
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# avoid divide-by-zero using where
df["PositivityRate"] = (df["Confirmed"] / df["Tests Conducted"].where(df["Tests Conducted"] != 0)).fillna(0)
df["CFR"] = (df["Deaths"] / df["Confirmed"].where(df["Confirmed"] != 0)).fillna(0)  # Case Fatality Ratio

# 4) Save cleaned/enhanced file
df.to_csv("covid19_cleaned_dataset.csv", index=False)
print("✅ Saved: covid19_cleaned_dataset.csv")
