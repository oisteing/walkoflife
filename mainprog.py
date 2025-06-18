import streamlit as st
import os
import csv
from datetime import date
import pandas as pd
import altair as alt

COUNTER_FILE = "counter.txt"
LOG_FILE = "log.csv"

# --- Utility functions ---
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

# --- App starts here ---
st.set_page_config(page_title="Walk Tracker", layout="centered")

# Reset button (top-left)
col_reset, col_title = st.columns([1, 4])
with col_reset:
    reset_pressed = st.button("🔁 Reset counter", key="reset")

# App title
with col_title:
    st.markdown("<h1 style='text-align: center;'>🚶‍♂️ Walk Tracker</h1>", unsafe_allow_html=True)

# Read counter
counter = 0 if reset_pressed else read_counter()

# Slider for meters
meters_per_walk = st.slider("Meters per walk", 0, 100, 10)

# --- Button styles ---
st.markdown("""
    <style>
    .stButton>button {
        height: 80px !important;
        width: 80px !important;
        font-size: 36px !important;
        border-radius: 50% !important;
        border: none;
        margin: 10px;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        transition: 0.2s;
    }
    div[data-testid="column"] button[title="R"] {
        background-color: #e74c3c !important; /* red */
        color: white !important;
    }
    div[data-testid="column"] button[title="Ø"] {
        background-color: #3498db !important; /* blue */
        color: white !important;
    }
    div[data-testid="column"] button:has-text("Reset counter") {
        background-color: #777 !important;
        color: white !important;
        border-radius: 6px !important;
        width: 100% !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Layout for R and Ø buttons
col1, col2 = st.columns(2)
clicks = 0
with col1:
    if st.button("R", key="R", help="Red button"):
        counter += 1
        clicks += 1
with col2:
    if st.button("Ø", key="Ø", help="Blue button"):
        counter += 1
        clicks += 1

# Write updated counter
write_counter(counter)
if clicks > 0:
    log_walks(clicks, meters_per_walk)

# Total
total_meters = counter * meters_per_walk
st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <h2>Walk count: {counter}</h2>
        <h3>Total meters walked: {total_meters} m</h3>
    </div>
""", unsafe_allow_html=True)

# --- Graph ---
if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE, names=["Date", "Meters"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Date:T', title="Date"),
        y=alt.Y('Meters:Q', title="Meters walked"),
        tooltip=['Date:T', 'Meters']
    ).properties(
        title="Meters walked per day",
        height=300
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No walk data yet.")
