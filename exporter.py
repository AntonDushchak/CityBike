"""Export utilities for cleaned data and summary tables."""

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from loader import save_csv

def export_clean_data(
    stations: Optional[pd.DataFrame],
    trips: Optional[pd.DataFrame],
    maintenance: Optional[pd.DataFrame],
    stations_path: str = "data/stations_clean.csv",
    trips_path: str = "data/trips_clean.csv",
    maintenance_path: str = "data/maintenance_clean.csv",
) -> Dict[str, str]:
    """Export cleaned datasets to CSV files.

    Args:
        stations: Cleaned stations DataFrame.
        trips: Cleaned trips DataFrame.
        maintenance: Cleaned maintenance DataFrame.
        stations_path: Output path for cleaned stations.
        trips_path: Output path for cleaned trips.
        maintenance_path: Output path for cleaned maintenance.

    Returns:
        Dictionary mapping dataset names to saved file paths.
    """
    exports: Dict[str, str] = {}
    if stations is not None:
        save_csv(stations_path, stations)
        exports["stations_clean"] = stations_path
    if trips is not None:
        save_csv(trips_path, trips)
        exports["trips_clean"] = trips_path
    if maintenance is not None:
        save_csv(maintenance_path, maintenance)
        exports["maintenance_clean"] = maintenance_path
    return exports

def export_summary_tables(
    metrics: Dict[str, object],
    output_dir: str = "output",
) -> Dict[str, str]:
    """Export top stations, top users, and maintenance summaries to CSV.

    Args:
        metrics: Dictionary of computed metrics from AnalyticsReporter.
        output_dir: Directory to save output CSV files.

    Returns:
        Dictionary mapping export names to saved file paths.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    exports: Dict[str, str] = {}

    top_stations = metrics.get("top_stations")
    combined_frames: List[pd.DataFrame] = []
    if isinstance(top_stations, dict):
        for role, df in top_stations.items():
            if df is not None and not df.empty:
                tmp = df.copy()
                tmp["station_role"] = role
                combined_frames.append(tmp)
    if combined_frames:
        stations_df = pd.concat(combined_frames, ignore_index=True)
        station_path = out_dir / "top_stations.csv"
        save_csv(str(station_path), stations_df)
        exports["top_stations"] = str(station_path)

    top_users = metrics.get("top_users")
    if isinstance(top_users, pd.DataFrame) and not top_users.empty:
        users_path = out_dir / "top_users.csv"
        save_csv(str(users_path), top_users)
        exports["top_users"] = str(users_path)

    maintenance_cost = metrics.get("maintenance_cost")
    if isinstance(maintenance_cost, pd.DataFrame) and not maintenance_cost.empty:
        cost_path = out_dir / "maintenance_costs.csv"
        save_csv(str(cost_path), maintenance_cost)
        exports["maintenance_costs"] = str(cost_path)

    maintenance_frequency = metrics.get("maintenance_frequency")
    if isinstance(maintenance_frequency, pd.DataFrame) and not maintenance_frequency.empty:
        freq_path = out_dir / "maintenance_frequency.csv"
        save_csv(str(freq_path), maintenance_frequency)
        exports["maintenance_frequency"] = str(freq_path)

    return exports