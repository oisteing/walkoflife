import streamlit as st
import os
import csv
from datetime import date
import pandas as pd
import altair as alt

COUNTER_FILE = "counter.txt"
LOG_FILE = "log.csv"

def read_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
        return 0
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

def write_counter(value):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value))

def log_walks(walks_today, meters_per_walk):
    today = date.today().isoformat()
    existing = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    existing[row[0]] = int(row[1])
    existing[today] = existing.get(today, 0) + walks_today * meters_per_walk
    with open(LOG_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        for d, meters in existing.items():
            writer.writerow([d, meters])

def reset_today():
    today = date.today().isoformat()
    existing = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    existing[row[0]] = int(row[1])
    existing[today] = 0
    with open(LOG_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        for d, meters in existing.items():
            writer.writerow([d, meters])

# -------------------------------
# INIT
# -------------------------------
st.set_page_config(page_title="Walk Tracker", layout="centered")

# Load counter
if "counter" not in st.session_state:
    st.session_state.counter = read_counter()
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

# -------------------------------
# STYLE: CSS som fungerer
# -------------------------------
st.markdown("""
<style>
button[kind="secondary"] {
    height: 100px !important;
    width: 100px !important;
    font-size: 36px !important;
    border-radius: 50% !important;
    color: white !important;
    border: none !important;
    margin: 10px !important;
}
div[data-testid="column"]:nth-of-type(1) button {
    background-color: #e74c3c !important;  /* R */
}
div[data-testid="column"]:nth-of-type(2) button {
    background-color: #3498db !important;  /* Ø */
}
button.reset-btn {
    background-color: #777 !important;
    color: white !important;
    border-radius: 6px !important;
    font-size: 14px !important;
    padding: 8px 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# UI: Reset + tittel
# -------------------------------
col_reset, col_title = st.columns([1, 4])
with col_reset:
    if st.button("🔁 Reset", key="reset"):
        st.session_state.counter = 0
        write_counter(0)
        reset_today()
with col_title:
    st.markdown("<h1 style='text-align: center;'>🚶‍♂️ Walk Tracker</h1>", unsafe_allow_html=True)

# -------------------------------
# Slider
# -------------------------------
meters_per_walk = st.slider("Meters per walk", 0, 100, 10)

# -------------------------------
# Runde knapper for R og Ø
# -------------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("R", key="rbtn"):
        st.session_state.counter += 1
        st.session_state.clicks += 1
with col2:
    if st.button("Ø", key="obtn"):
        st.session_state.counter += 1
        st.session_state.clicks += 1

# -------------------------------
# Lagring og visning
# -------------------------------
write_counter(st.session_state.counter)
if st.session_state.clicks > 0:
    log_walks(st.session_state.clicks, meters_per_walk)
    st.session_state.clicks = 0

total_meters = st.session_state.counter * meters_per_walk
st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <h2>Walk count: {st.session_state.counter}</h2>
        <h3>Total meters walked: {total_meters} m</h3>
    </div>
""", unsafe_allow_html=True)

# -------------------------------
# Bar graph
# -------------------------------
if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE, names=["Date", "Meters"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Date:T', title="Date"),
        y=alt.Y('Meters:Q', title="Meters walked"),
        tooltip=["Date:T", "Meters"]
    ).properties(
        title="Meters walked per day",
        height=300
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No walk data yet.")
