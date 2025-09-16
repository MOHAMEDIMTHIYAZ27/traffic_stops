import streamlit as st
import pandas as pd

st.set_page_config(page_title="Traffic Stops Dashboard", layout="wide")

# --- Load dataset ---
try:
    df = pd.read_csv(r"C:\Users\user\Downloads\police_stops.csv.csv")
except FileNotFoundError:
    st.error("File 'traffic_stops.csv' not found in the current directory.")
    st.stop()

# --- Clean column names ---
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# --- Show columns to debug ---
st.write("### Available columns in dataset:")
st.write(list(df.columns))

st.title("Traffic Stops Dashboard")

# --- Sidebar filters (auto-generated for existing columns) ---
st.sidebar.header("Filter Data")

for col in df.columns:
    unique_vals = df[col].dropna().unique()
    if len(unique_vals) < 50:  # Only create filter for categorical columns
        selected_vals = st.sidebar.multiselect(
            f"Filter by {col.replace('_', ' ').title()}",
            options=sorted(unique_vals),
            default=[]
        )
        if selected_vals:
            df = df[df[col].isin(selected_vals)]

# --- Display filtered data ---
st.subheader("Filtered Data")
st.dataframe(df)

# --- Summary statistics ---
if not df.empty:
    st.subheader("Summary Statistics")
    st.write(df.describe(include="all"))
else:
    st.warning("No data available after applying filters.")
