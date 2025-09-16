DROP TABLE IF EXISTS police_stops;

CREATE TABLE police_stops (
    stop_date TEXT,
    stop_time TEXT,
    country_name TEXT,
    driver_gender TEXT,
    driver_age_raw INTEGER,
    driver_age INTEGER,
    driver_race TEXT,
    violation_raw TEXT,
    violation TEXT,
    search_conducted INTEGER,
    search_type TEXT,
    stop_outcome TEXT,
    is_arrested INTEGER,
    stop_duration TEXT,
    drugs_related_stop INTEGER,
    vehicle_number TEXT
);
