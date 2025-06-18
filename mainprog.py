import streamlit as st
import os

COUNTER_FILE = "counter.txt"

# Functions to handle the counter
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

# Read current counter value
counter = read_counter()

# Page setup
st.set_page_config(page_title="Walk Tracker", layout="centered")

# App title
st.markdown("<h1 style='text-align: center;'>🚶‍♂️ Walk Tracker</h1>", unsafe_allow_html=True)

# Slider for meters per walk
meters_per_walk = st.slider("Meters per walk", 0, 100, 10)

# Inject custom CSS for button styling
st.markdown("""
    <style>
    div.stButton > button {
        height: 80px;
        width: 80px;
        font-size: 36px;
        border-radius: 40px;
        background-color: #4CAF50;
        color: white;
        border: none;
        margin: 10px;
    }
    div.stButton > button:hover {
        background-color: #45a049;
        transition: 0.2s;
    }
    .reset-btn button {
        background-color: #d9534f !important;
        border-radius: 12px;
        width: 100%;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Button layout
col1, col2, col3 = st.columns([1, 1, 1.2])
with col1:
    if st.button("R", key="R"):
        counter += 1
        write_counter(counter)
with col2:
    if st.button("Ø", key="Ø"):
        counter += 1
        write_counter(counter)
with col3:
    with st.container():
        if st.button("Reset", key="reset"):
            counter = 0
            write_counter(counter)

# Show counter and total meters
total_meters = counter * meters_per_walk

st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <h2>Walk count: {counter}</h2>
        <h3>Total meters walked: {total_meters} m</h3>
    </div>
""", unsafe_allow_html=True)
