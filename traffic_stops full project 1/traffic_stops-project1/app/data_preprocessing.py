import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)
    df = df.drop_duplicates()
    df = df.fillna("Unknown")
    df["stop_date"] = pd.to_datetime(df["stop_date"], errors="coerce")
    df["driver_age"] = pd.to_numeric(df["driver_age"], errors="coerce")
    df["stop_datetime"] = df["stop_date"].astype(str) + " " + df["stop_time"]
    return df
