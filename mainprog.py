import streamlit as st
import os
import csv
from datetime import date
import pandas as pd
import altair as alt

COUNTER_FILE = "counter.txt"
LOG_FILE = "log.csv"

# --- Hjelpefunksjoner ---
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

# --- Oppsett ---
st.set_page_config(page_title="Walk Tracker", layout="centered")

if "counter" not in st.session_state:
    st.session_state.counter = read_counter()
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

# --- STIL ---
st.markdown("""
<style>
button.r-button {
    background-color: #e74c3c !important;
    color: white !important;
    height: 100px !important;
    width: 100px !important;
    border-radius: 50% !important;
    font-size: 36px !important;
    border: none !important;
    margin: 10px;
}
button.o-button {
    background-color: #3498db !important;
    color: white !important;
    height: 100px !important;
    width: 100px !important;
    border-radius: 50% !important;
    font-size: 36px !important;
    border: none !important;
    margin: 10px;
}
button.reset-button {
    background-color: #777 !important;
    color: white !important;
    border-radius: 6px !important;
    font-size: 16px !important;
    padding: 8px 12px !important;
}
</style>
""", unsafe_allow_html=True)

# --- Topp: reset og tittel ---
col_reset, col_title = st.columns([1, 4])
with col_reset:
    if st.button("🔁 Reset", key="reset", help="Reset counter and today's log"):
        st.session_state.counter = 0
        write_counter(0)
        reset_today()
with col_title:
    st.markdown("<h1 style='text-align: center;'>🚶‍♂️ Walk Tracker</h1>", unsafe_allow_html=True)

# --- Slider ---
meters_per_walk = st.slider("Meters per walk", 0, 100, 10)

# --- Runde knapper: R og Ø ---
col1, col2 = st.columns(2)
with col1:
    st.markdown('<button class="r-button" onclick="fetch(\'/R\')">R</button>', unsafe_allow_html=True)
    if st.button(" ", key="r_real"):
        st.session_state.counter += 1
        st.session_state.clicks += 1

with col2:
    st.markdown('<button class="o-button" onclick="fetch(\'/Ø\')">Ø</button>', unsafe_allow_html=True)
    if st.button(" ", key="o_real"):
        st.session_state.counter += 1
        st.session_state.clicks += 1

# --- Lagre og visning ---
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

# --- Graf ---
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
