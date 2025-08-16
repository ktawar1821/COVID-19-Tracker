import logging, os
from datetime import datetime
import pandas as pd, random
from datetime import datetime, timedelta

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

try:
    # --- Generate (same logic you used) ---
    random.seed(42)
    start_date = datetime(2020, 3, 1); end_date = datetime(2021, 2, 28)
    countries = ["India","USA","Brazil","Italy","South Africa"]
    states = {
        "India":["Maharashtra","Kerala","Delhi"],
        "USA":["New York","California","Texas"],
        "Brazil":["São Paulo","Rio de Janeiro","Bahia"],
        "Italy":["Lombardy","Lazio","Veneto"],
        "South Africa":["Gauteng","KwaZulu-Natal","Western Cape"]
    }
    rows=[]; cur=start_date
    while cur<=end_date:
        for c in countries:
            for s in states[c]:
                confirmed = random.randint(0, 5000)
                deaths = random.randint(0, int(confirmed*0.05))
                recovered = random.randint(0, confirmed - deaths)
                active = confirmed - deaths - recovered
                tests_conducted = confirmed + random.randint(1000, 10000)
                rows.append({"Date":cur.strftime("%Y-%m-%d"),"Country":c,"State/Province":s,
                             "Confirmed":confirmed,"Deaths":deaths,"Recovered":recovered,
                             "Active":active,"Tests Conducted":tests_conducted})
        cur += timedelta(days=1)
    raw = pd.DataFrame(rows)

    # --- Clean/feature ---
    raw["Date"]=pd.to_datetime(raw["Date"])
    num_cols=["Confirmed","Deaths","Recovered","Active","Tests Conducted"]
    raw = raw[(raw[num_cols] >= 0).all(axis=1)].drop_duplicates()
    raw["PositivityRate"] = (raw["Confirmed"] / raw["Tests Conducted"].where(raw["Tests Conducted"]!=0)).fillna(0)
    raw["CFR"] = (raw["Deaths"] / raw["Confirmed"].where(raw["Confirmed"]!=0)).fillna(0)

    raw.to_csv("covid19_cleaned_dataset.csv", index=False)
    logging.info("Pipeline success: rows=%d", len(raw))
except Exception as e:
    logging.exception("Pipeline failed")
    raise
