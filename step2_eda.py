import pandas as pd

df = pd.read_csv("covid19_cleaned_dataset.csv", parse_dates=["Date"])

# Country-level daily totals
daily_country = (df.groupby(["Date","Country"], as_index=False)
                   [["Confirmed","Deaths","Recovered","Active","Tests Conducted"]].sum())

# Monthly summaries per country
monthly_country = (df.groupby(["Month","Country"], as_index=False)
                     [["Confirmed","Deaths","Recovered","Active","Tests Conducted"]].sum())

# Top 5 states by total confirmed
state_totals = (df.groupby(["Country","State/Province"], as_index=False)["Confirmed"].sum()
                  .sort_values("Confirmed", ascending=False).head(5))

print("Daily country totals (head):\n", daily_country.head(), "\n")
print("Monthly country totals (head):\n", monthly_country.head(), "\n")
print("Top 5 states by Confirmed:\n", state_totals, "\n")

daily_country.to_csv("agg_daily_country.csv", index=False)
monthly_country.to_csv("agg_monthly_country.csv", index=False)
state_totals.to_csv("top_states_confirmed.csv", index=False)
print("✅ Saved: agg_daily_country.csv, agg_monthly_country.csv, top_states_confirmed.csv")
