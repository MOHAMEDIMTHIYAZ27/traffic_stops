import sqlite3
import pandas as pd

# Paths
DB_PATH = r"C:\Users\user\traffic_stops-project1\database\police_stops.db"
CSV_PATH = r"C:\Users\user\traffic_stops-project1\database\police_stops.csv"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Insert into table
df.to_sql("police_stops", conn, if_exists="append", index=False)

conn.close()
print("✅ Data loaded successfully into police_stops table!")
