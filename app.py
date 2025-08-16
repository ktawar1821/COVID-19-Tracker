import logging, os, time
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.info("App start")

# small helper for file mtime (data freshness)
def file_mtime(path):
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
    except Exception:
        return "N/A"



import streamlit as st
import pandas as pd

st.set_page_config(page_title="COVID-19 Tracker (Offline)", layout="wide")
st.title("📊 COVID-19 Data Tracker (Offline)")

@st.cache_data
def load_data(path: str):
    return pd.read_csv(path, parse_dates=["Date"])

# 1) Load with error handling
# 1) Load with error handling
DATA_PATH = "covid19_cleaned_dataset.csv"
try:
    df = load_data(DATA_PATH)
    logging.info(f"Loaded dataset successfully: {len(df)} rows")
except Exception as e:
    logging.exception("Failed to load dataset")
    st.error(f"Could not load `{DATA_PATH}`. Error: {e}")
    st.info("Make sure you've run `python step1_clean.py` to create the cleaned dataset.")
    st.stop()

# 2) Show last updated timestamp in UI
st.caption(f"🔄 Data file: `{DATA_PATH}`  •  Last updated: {file_mtime(DATA_PATH)}")



# 2) Sidebar filters (always render something)
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Country", sorted(df["Country"].unique()))
states = sorted(df.loc[df["Country"] == country, "State/Province"].unique())
state = st.sidebar.selectbox("State/Province", states)

# 3) Filtered slice
slice_df = df[(df["Country"] == country) & (df["State/Province"] == state)].sort_values("Date")

# 4) KPIs
total_confirmed = int(slice_df["Confirmed"].sum())
total_deaths = int(slice_df["Deaths"].sum())
total_recovered = int(slice_df["Recovered"].sum())
tests_total = int(slice_df["Tests Conducted"].sum())
positivity = (total_confirmed / tests_total * 100) if tests_total else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Confirmed", f"{total_confirmed:,}")
c2.metric("Total Deaths", f"{total_deaths:,}")
c3.metric("Total Recovered", f"{total_recovered:,}")
c4.metric("Positivity Rate", f"{positivity:.2f}%")

st.subheader(f"Daily Trends — {state}, {country}")

# 5) Use Streamlit’s native charts (less brittle than matplotlib here)
st.line_chart(slice_df.set_index("Date")[["Confirmed"]].rename(columns={"Confirmed":"Confirmed (daily)"}))

slice_df = slice_df.copy()
slice_df["Confirmed_7d"] = slice_df["Confirmed"].rolling(7, min_periods=1).mean()
st.line_chart(slice_df.set_index("Date")[["Confirmed_7d"]])

# 6) Monthly bar chart by country (not just the selected state)
df = df.copy()
df["Month"] = df["Date"].dt.to_period("M").astype(str)
monthly = (df[df["Country"] == country]
           .groupby("Month", as_index=False)["Confirmed"].sum()
           .sort_values("Month"))
st.subheader(f"Monthly Confirmed — {country}")
st.bar_chart(monthly.set_index("Month"))
