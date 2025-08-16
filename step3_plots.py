import pandas as pd
import matplotlib.pyplot as plt

# 1) Load
df = pd.read_csv("covid19_cleaned_dataset.csv", parse_dates=["Date"])

# 2) Line chart: India daily confirmed + 7d avg
india = (df[df["Country"] == "India"]
         .groupby("Date", as_index=False)[["Confirmed","Deaths","Recovered","Active","Tests Conducted"]]
         .sum())
india["Confirmed_7d"] = india["Confirmed"].rolling(7, min_periods=1).mean()

plt.figure()
plt.plot(india["Date"], india["Confirmed"], label="Confirmed (daily)")
plt.plot(india["Date"], india["Confirmed_7d"], label="Confirmed (7d avg)")
plt.title("India — Daily Confirmed & 7-day Avg")
plt.xlabel("Date"); plt.ylabel("Count"); plt.legend()
plt.tight_layout()
plt.savefig("plot_india_confirmed.png")

# 3) Bar chart: Monthly confirmed by country
df["Month"] = df["Date"].dt.to_period("M").astype(str)   # <-- create a named column
monthly = (df.groupby(["Month","Country"], as_index=False)["Confirmed"].sum())

pivot = monthly.pivot(index="Month", columns="Country", values="Confirmed").fillna(0)
# (Optional) sanity check:
# print(pivot.head())

plt.figure()
pivot.plot(kind="bar")
plt.title("Monthly Confirmed by Country")
plt.xlabel("Month"); plt.ylabel("Confirmed")
plt.tight_layout()
plt.savefig("plot_monthly_countries.png")

print("✅ Saved plots: plot_india_confirmed.png, plot_monthly_countries.png")
