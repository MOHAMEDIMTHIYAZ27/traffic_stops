import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "database/police_stops.db"

# Helper function: run queries
def run_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Helper function: insert new violation
def insert_violation(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO police_stops (
            stop_date, stop_time, country_name, driver_gender,
            driver_age_raw, driver_age, driver_race,
            violation_raw, violation,
            search_conducted, search_type, stop_outcome,
            is_arrested, stop_duration, drugs_related_stop, vehicle_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

# Streamlit App
st.set_page_config(page_title="Police Stops Dashboard", layout="wide")
st.title("🚔 Police Stops Dashboard")

# --- Load Original Data ---
df_original = run_query("SELECT * FROM police_stops")

# --- Sidebar Filters (Dynamic) ---
st.sidebar.header("🔍 Filter Data")

filters = {}
for col in df_original.columns:
    unique_vals = df_original[col].dropna().unique()
    if df_original[col].dtype == "object":
        selected = st.sidebar.multiselect(f"{col}", ["All"] + sorted(unique_vals.astype(str)))
        if "All" not in selected and selected:
            filters[col] = selected
    elif pd.api.types.is_numeric_dtype(df_original[col]):
        min_val, max_val = float(df_original[col].min()), float(df_original[col].max())
        selected_range = st.sidebar.slider(f"{col}", min_val, max_val, (min_val, max_val))
        filters[col] = selected_range
    else:
        pass

# --- Apply Filters ---
df_filtered = df_original.copy()

for col, val in filters.items():
    if isinstance(val, list):  # categorical
        df_filtered = df_filtered[df_filtered[col].isin(val)]
    elif isinstance(val, tuple):  # numeric range
        df_filtered = df_filtered[(df_filtered[col] >= val[0]) & (df_filtered[col] <= val[1])]

# --- Display Data ---
st.subheader("📊 Original Dataset")
st.dataframe(df_original, use_container_width=True)

st.subheader("📊 Filtered Dataset")
st.dataframe(df_filtered, use_container_width=True)

# --- Register New Violation ---
st.sidebar.header("📝 Register New Violation")

with st.sidebar.form("new_violation_form"):
    stop_date = st.text_input("Stop Date (YYYY-MM-DD)")
    stop_time = st.text_input("Stop Time (HH:MM)")
    country_name = st.text_input("Country")
    driver_gender = st.selectbox("Driver Gender", ["M", "F", "Other"])
    driver_age_raw = st.number_input("Driver Age Raw", min_value=0, step=1)
    driver_age = st.number_input("Driver Age", min_value=0, step=1)
    driver_race = st.text_input("Driver Race")
    violation_raw = st.text_input("Violation Raw")
    violation = st.text_input("Violation")
    search_conducted = st.checkbox("Search Conducted", value=False)
    search_type = st.text_input("Search Type")
    stop_outcome = st.text_input("Stop Outcome")
    is_arrested = st.checkbox("Is Arrested", value=False)
    stop_duration = st.text_input("Stop Duration")
    drugs_related_stop = st.checkbox("Drugs Related Stop", value=False)
    vehicle_number = st.text_input("Vehicle Number")

    submitted = st.form_submit_button("Add Record")

    if submitted:
        new_data = (
            stop_date, stop_time, country_name, driver_gender,
            driver_age_raw, driver_age, driver_race,
            violation_raw, violation,
            int(search_conducted), search_type, stop_outcome,
            int(is_arrested), stop_duration, int(drugs_related_stop), vehicle_number
        )
        insert_violation(new_data)
        st.success("✅ New violation registered successfully!")
