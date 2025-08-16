import pandas as pd

# Load dataset
df = pd.read_csv("covid19_medium_dataset.csv", parse_dates=["Date"])

# See the first 5 rows
print("First 5 rows:\n", df.head(), "\n")

# Basic info about columns & data types
print("\nDataset info:")
print(df.info())

# Summary statistics (numeric columns)
print("\nSummary statistics:")
print(df.describe())

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())
