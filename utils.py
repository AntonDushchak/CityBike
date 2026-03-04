"""Validation, formatting, and helper functions for data cleaning."""

from datetime import datetime
from typing import Optional, Union

import pandas as pd

from models import BIKE_TYPES, USER_TYPES

def validate_data_trips(trip: pd.DataFrame) -> pd.Series:
    """Return boolean mask for valid trip rows in DataFrame.

    Args:
        trip: DataFrame containing trip data.

    Returns:
        Boolean Series where True indicates a valid row.
    """
    required = [
        "trip_id", "user_id", "user_type", "bike_id", "bike_type",
        "start_station_id", "end_station_id", "start_time", "end_time",
        "duration_minutes", "distance_km", "status",
    ]
    mask = trip[required].notnull().all(axis=1)
    mask &= trip["duration_minutes"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)
    mask &= trip["distance_km"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)
    mask &= trip["end_time"] >= trip["start_time"]
    return mask

def validate_data_stations(station: pd.DataFrame) -> pd.Series:
    """Return boolean mask for valid station rows in DataFrame.

    Args:
        station: DataFrame containing station data.

    Returns:
        Boolean Series where True indicates a valid row.
    """
    required = ["station_id", "station_name", "capacity", "latitude", "longitude"]
    mask = station[required].notnull().all(axis=1)
    mask &= station["capacity"].apply(lambda x: isinstance(x, (int, float)) and x >= 1)
    mask &= station["latitude"].apply(lambda x: isinstance(x, (int, float)) and -90 <= x <= 90)
    mask &= station["longitude"].apply(lambda x: isinstance(x, (int, float)) and -180 <= x <= 180)
    return mask

def validate_data_maintenance(maintenance: pd.DataFrame) -> pd.Series:
    """Return boolean mask for valid maintenance rows in DataFrame.

    Args:
        maintenance: DataFrame containing maintenance data.

    Returns:
        Boolean Series where True indicates a valid row.
    """
    required = [
        "record_id", "bike_id", "bike_type", "date",
        "maintenance_type", "cost", "description",
    ]
    mask = maintenance[required].notnull().all(axis=1)
    mask &= maintenance["cost"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)
    return mask

def clean_data_trips(trips: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize trip data in DataFrame.

    Args:
        trips: Raw trip DataFrame.

    Returns:
        Cleaned DataFrame with valid rows only.
    """
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

def clean_data_stations(stations: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize station data in DataFrame.

    Args:
        stations: Raw station DataFrame.

    Returns:
        Cleaned DataFrame with valid rows only.
    """
    df = stations.copy()

    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df["station_name"] = df["station_name"].astype(str).str.strip()

    df = df.drop_duplicates()

    mask = validate_data_stations(df)
    df = df[mask]
    return df

def clean_data_maintenance(maintenance: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize maintenance data in DataFrame.

    Args:
        maintenance: Raw maintenance DataFrame.

    Returns:
        Cleaned DataFrame with valid rows only.
    """
    df = maintenance.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce")

    df["maintenance_type"] = df["maintenance_type"].astype(str).str.lower().str.strip()
    df["description"] = df["description"].astype(str).str.strip()

    df = df.drop_duplicates()

    mask = validate_data_maintenance(df)
    df = df[mask]
    return df

def clean_data_users(trips: pd.DataFrame) -> pd.DataFrame:
    """Create cleaned users DataFrame from trips data.

    Args:
        trips: Cleaned trips DataFrame.

    Returns:
        DataFrame with unique users and their types.
    """
    df = trips.copy()
    
    df["user_id"] = df["user_id"].astype(str)
    df["user_type"] = df["user_type"].astype(str).str.lower().str.strip()
    
    users_df = df[["user_id", "user_type"]].drop_duplicates(subset=["user_id"])
    
    users_df = users_df.dropna()
    
    users_df = users_df[users_df["user_type"].isin(USER_TYPES)]
    
    return users_df.reset_index(drop=True)

def clean_data_bikes(trips: pd.DataFrame, maintenance: pd.DataFrame) -> pd.DataFrame:
    """Create cleaned bikes DataFrame from trips and maintenance data.

    Args:
        trips: Cleaned trips DataFrame.
        maintenance: Cleaned maintenance DataFrame.

    Returns:
        DataFrame with unique bikes, their types, and statuses.
    """
    trips_df = trips.copy()
    maintenance_df = maintenance.copy()
    
    trips_bikes = trips_df[["bike_id", "bike_type"]].copy()
    trips_bikes["status"] = "available"
    
    maintenance_bikes = maintenance_df[["bike_id", "bike_type"]].copy()
    maintenance_bikes["status"] = "maintenance"
    
    bikes_df = pd.concat([trips_bikes, maintenance_bikes], ignore_index=True)
    
    bikes_df["bike_id"] = bikes_df["bike_id"].astype(str)
    bikes_df["bike_type"] = bikes_df["bike_type"].astype(str).str.lower().str.strip()
    bikes_df["status"] = bikes_df["status"].astype(str).str.lower().str.strip()
    
    bikes_df = bikes_df.drop_duplicates(subset=["bike_id"], keep="first")
    
    bikes_df = bikes_df.dropna()
    
    bikes_df = bikes_df[bikes_df["bike_type"].isin(BIKE_TYPES)]
    
    return bikes_df.reset_index(drop=True)

def format_duration(seconds: Union[int, float]) -> Optional[str]:
    """Format duration in human-readable format (e.g., 1h 2m 3s).

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted string or None if invalid.
    """
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

def format_date(timestamp: Union[str, int, float, datetime, None]) -> Optional[datetime]:
    """Parse various timestamp formats into a datetime object.

    Args:
        timestamp: Input timestamp (string, number, or datetime).

    Returns:
        Parsed datetime or None if invalid.
    """
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