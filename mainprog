import streamlit as st
import os

COUNTER_FILE = "counter.txt"

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

# Initialize counter
counter = read_counter()

st.set_page_config(page_title="Walk Tracker", layout="centered")

st.title("🚶‍♂️ Walk Tracker")

# Slider
meters = st.slider("Meters covered per walk", 0, 100, 10)

# Layout for buttons
col1, col2, col3 = st.columns([1, 1, 1.2])
with col1:
    if st.button("🅁", key="R", use_container_width=True):
        counter += 1
        write_counter(counter)
with col2:
    if st.button("Ø", key="O", use_container_width=True):
        counter += 1
        write_counter(counter)
with col3:
    if st.button("🔁 Reset", key="Reset", use_container_width=True):
        counter = 0
        write_counter(counter)

# Show counter
st.markdown(
    f"""
    <div style="font-size:48px; text-align:center; margin-top:20px;">
        Total Walks: <strong>{counter}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

# Display meters
st.markdown(
    f"""
    <div style="font-size:24px; text-align:center; margin-top:10px;">
        Each walk covers: <strong>{meters} meters</strong>
    </div>
    """,
    unsafe_allow_html=True
)
