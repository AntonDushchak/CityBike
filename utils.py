"""
Validation, formatting, helpers
"""

import pandas as pd
from datetime import datetime

def validate_data_trips(trip):
    """Return boolean mask for valid trip rows in DataFrame"""
    required = ["trip_id", "user_id", "user_type", "bike_id", "bike_type", "start_station_id", "end_station_id", "start_time", "end_time", "duration_minutes", "distance_km", "status"]
    mask = trip[required].notnull().all(axis=1)
    mask &= trip["duration_minutes"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)
    mask &= trip["distance_km"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)
    return mask

def validate_data_stations(station):
    """Return boolean mask for valid station rows in DataFrame"""
    required = ["station_id", "station_name", "capacity", "latitude", "longitude"]
    mask = station[required].notnull().all(axis=1)
    mask &= station["capacity"].apply(lambda x: isinstance(x, (int, float)) and x >= 1)
    mask &= station["latitude"].apply(lambda x: isinstance(x, (int, float)) and -90 <= x <= 90)
    mask &= station["longitude"].apply(lambda x: isinstance(x, (int, float)) and -180 <= x <= 180)
    return mask

def validate_data_maintenance(maintenance):
    """Return boolean mask for valid maintenance rows in DataFrame"""
    required = ["record_id", "bike_id", "bike_type", "date", "maintenance_type", "cost", "description"]
    mask = maintenance[required].notnull().all(axis=1)
    mask &= maintenance["cost"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)
    return mask

def clean_data_trips(trips):
    """Clean and standardize trip data in DataFrame"""
    df = trips.copy()

    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")

    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")
    df["distance_km"] = pd.to_numeric(df["distance_km"], errors="coerce")

    df["user_type"] = df["user_type"].astype(str).str.lower().str.strip()
    df["bike_type"] = df["bike_type"].astype(str).str.lower().str.strip()
    df["status"] = df["status"].astype(str).str.lower().str.strip()

    df = df.drop_duplicates()

    mask = validate_data_trips(df)
    df = df[mask]
    return df

def clean_data_stations(stations):
    """Clean and standardize station data in DataFrame"""
    df = stations.copy()

    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df["station_name"] = df["station_name"].astype(str).str.strip()

    df = df.drop_duplicates()

    mask = validate_data_stations(df)
    df = df[mask]
    return df

def clean_data_maintenance(maintenance):
    """Clean and standardize maintenance data in DataFrame"""
    df = maintenance.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce")

    df["maintenance_type"] = df["maintenance_type"].astype(str).str.lower().str.strip()
    df["description"] = df["description"].astype(str).str.strip()

    df = df.drop_duplicates()

    mask = validate_data_maintenance(df)
    df = df[mask]
    return df

def format_duration(seconds):
    """Format duration in human-readable format (e.g., 1h 2m 3s). Returns None if invalid."""
    try:
        if not isinstance(seconds, (int, float)) or seconds < 0:
            return None
        seconds = int(seconds)
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        parts = []
        if h > 0:
            parts.append(f"{h}h")
        if m > 0:
            parts.append(f"{m}m")
        if s > 0 or not parts:
            parts.append(f"{s}s")
        return " ".join(parts)
    except Exception:
        return None

def format_date(timestamp):
    """Format date in standard format. Returns datetime or None if invalid."""
    try:
        if timestamp is None:
            return None
        if isinstance(timestamp, datetime):
            return timestamp
        if isinstance(timestamp, str):
            try:
                return datetime.fromisoformat(timestamp)
            except Exception:
                pass
            try:
                return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return None
        if isinstance(timestamp, (int, float)):
            if timestamp < 0:
                return None
            return datetime.fromtimestamp(timestamp)
    except Exception:
        return None
    return None