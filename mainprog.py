import streamlit as st
import os
import csv
from datetime import date
import pandas as pd
import altair as alt

COUNTER_FILE = "counter.txt"
LOG_FILE = "log.csv"

# --- Funksjoner for filhåndtering ---
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

# --- Start konfigurasjon ---
st.set_page_config(page_title="Walk Tracker", layout="centered")

# --- Initiering av tilstand ---
if "counter" not in st.session_state:
    st.session_state.counter = read_counter()
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

# --- Styling: Runde knapper og farger ---
st.markdown("""
<style>
.styled-button {
    height: 100px !important;
    width: 100px !important;
    font-size: 36px !important;
    border-radius: 50% !important;
    border: none !important;
    margin: 10px !important;
    color: white !important;
}
</style>
<script>
const buttons = window.parent.document.querySelectorAll('button');
buttons.forEach(btn => {
    if (btn.innerText === "R") {
        btn.classList.add("styled-button");
        btn.style.backgroundColor = "#e74c3c";
    }
    if (btn.innerText === "Ø") {
        btn.classList.add("styled-button");
        btn.style.backgroundColor = "#3498db";
    }
    if (btn.innerText === "🔁 Reset") {
        btn.style.backgroundColor = "#777";
        btn.style.color = "white";
        btn.style.borderRadius = "6px";
        btn.style.fontSize = "14px";
        btn.style.padding = "8px 12px";
    }
});
</script>
""", unsafe_allow_html=True)

# --- Øverste rad: Reset og tittel ---
col_reset, col_title = st.columns([1, 4])
with col_reset:
    if st.button("🔁 Reset"):
        st.session_state.counter = 0
        write_counter(0)
        reset_today()
with col_title:
    st.markdown("<h1 style='text-align: center;'>🚶‍♂️ Walk Tracker</h1>", unsafe_allow_html=True)

# --- Slider for meter per walk ---
meters_per_walk = st.slider("Meters per walk", 0, 100, 10)

# --- Knappene: R og Ø ---
col1, col2 = st.columns(2)
with col1:
    if st.button("R"):
        st.session_state.counter += 1
        st.session_state.clicks += 1
with col2:
    if st.button("Ø"):
        st.session_state.counter += 1
        st.session_state.clicks += 1

# --- Oppdatering og logging ---
write_counter(st.session_state.counter)
if st.session_state.clicks > 0:
    log_walks(st.session_state.clicks, meters_per_walk)
    st.session_state.clicks = 0

# --- Visning av totalsum ---
total_meters = st.session_state.counter * meters_per_walk
st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <h2>Walk count: {st.session_state.counter}</h2>
        <h3>Total meters walked: {total_meters} m</h3>
    </div>
""", unsafe_allow_html=True)

# --- Graf over loggede meter per dag ---
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
