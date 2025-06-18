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

st.set_page_config(page_title="Walk Tracker", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .round-button {
        height: 100px;
        width: 100px;
        font-size: 40px;
        border-radius: 50%;
        border: none;
        margin: 10px;
        color: white;
        cursor: pointer;
    }
    .red { background-color: #e74c3c; }
    .blue { background-color: #3498db; }
    .reset-button {
        background-color: #777;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Reset and title
col_reset, col_title = st.columns([1, 4])
with col_reset:
    if st.button("🔁 Reset", key="reset"):
        write_counter(0)
        reset_today()
        counter = 0
    else:
        counter = read_counter()
with col_title:
    st.markdown("<h1 style='text-align: center;'>🚶‍♂️ Walk Tracker</h1>", unsafe_allow_html=True)

# --- Slider
meters_per_walk = st.slider("Meters per walk", 0, 100, 10)

# --- Custom round buttons with HTML
col1, col2 = st.columns(2)
clicks = 0

with col1:
    if st.markdown(
        '<form action="" method="post"><button name="r_btn" class="round-button red">R</button></form>',
        unsafe_allow_html=True
    ):
        pass
if st.session_state.get("r_btn"):
    counter += 1
    clicks += 1
    st.session_state["r_btn"] = False  # reset

with col2:
    if st.markdown(
        '<form action="" method="post"><button name="ø_btn" class="round-button blue">Ø</button></form>',
        unsafe_allow_html=True
    ):
        pass
if st.session_state.get("ø_btn"):
    counter += 1
    clicks += 1
    st.session_state["ø_btn"] = False  # reset

# Fallback for standard buttons (Streamlit limitation: workaround HTML can't trigger server-side events directly)
col1b, col2b = st.columns(2)
with col1b:
    if st.button("R", key="R_real"):
        counter += 1
        clicks += 1
with col2b:
    if st.button("Ø", key="Ø_real"):
        counter += 1
        clicks += 1

write_counter(counter)
if clicks > 0:
    log_walks(clicks, meters_per_walk)

# --- Totals
total_meters = counter * meters_per_walk
st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <h2>Walk count: {counter}</h2>
        <h3>Total meters walked: {total_meters} m</h3>
    </div>
""", unsafe_allow_html=True)

# --- Graph
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
