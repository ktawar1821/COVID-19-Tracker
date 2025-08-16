import pandas as pd
import random
from datetime import datetime, timedelta

# For reproducibility
random.seed(42)

start_date = datetime(2020, 3, 1)
end_date   = datetime(2021, 2, 28)

countries = ["India", "USA", "Brazil", "Italy", "South Africa"]
states = {
    "India": ["Maharashtra", "Kerala", "Delhi"],
    "USA": ["New York", "California", "Texas"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Bahia"],
    "Italy": ["Lombardy", "Lazio", "Veneto"],
    "South Africa": ["Gauteng", "KwaZulu-Natal", "Western Cape"]
}

rows = []
cur = start_date
while cur <= end_date:
    for country in countries:
        for state in states[country]:
            confirmed = random.randint(0, 5000)
            deaths = random.randint(0, int(confirmed * 0.05))
            recovered = random.randint(0, confirmed - deaths)
            active = confirmed - deaths - recovered
            tests_conducted = confirmed + random.randint(1000, 10000)

            rows.append({
                "Date": cur.strftime("%Y-%m-%d"),
                "Country": country,
                "State/Province": state,
                "Confirmed": confirmed,
                "Deaths": deaths,
                "Recovered": recovered,
                "Active": active,
                "Tests Conducted": tests_conducted
            })
    cur += timedelta(days=1)

df = pd.DataFrame(rows)
df.to_csv("covid19_medium_dataset.csv", index=False)

print(f"✅ Dataset created: {len(df)} rows saved to covid19_medium_dataset.csv")
