import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "police_stops.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

print("Looking for schema at:", SCHEMA_PATH)

if not os.path.exists(SCHEMA_PATH):
    raise FileNotFoundError(f"❌ schema.sql not found at {SCHEMA_PATH}")

# Connect to (or create) database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SCHEMA_PATH, "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Database and schema created successfully!")
