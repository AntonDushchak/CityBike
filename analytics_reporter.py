"""Analytics helpers for CityBike."""

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


class AnalyticsReporter:
    """Compute KPIs and format a plain-text report."""

    def __init__(self, users_df, bikes_df, stations_df, trips_df, maintenance_df):
        self.users = users_df if users_df is not None else pd.DataFrame()
        self.bikes = bikes_df if bikes_df is not None else pd.DataFrame()
        self.stations = stations_df if stations_df is not None else pd.DataFrame()
        self.trips = trips_df if trips_df is not None else pd.DataFrame()
        self.maintenance = maintenance_df if maintenance_df is not None else pd.DataFrame()

        if not self.trips.empty:
            for column in ("start_time", "end_time"):
                if column in self.trips.columns and not pd.api.types.is_datetime64_any_dtype(self.trips[column]):
                    self.trips[column] = pd.to_datetime(self.trips[column], errors="coerce")

    def compute_metrics(self) -> Dict[str, object]:
        metrics: Dict[str, object] = {}
        metrics["trip_summary"] = self._trip_summary()
        metrics["top_stations"] = self._top_stations()
        metrics["peak_hours"] = self._peak_hours()
        metrics["weekday_volume"] = self._weekday_volume()
        metrics["distance_by_user_type"] = self._distance_by_user_type()
        metrics["bike_utilization"] = self._bike_utilization()
        metrics["monthly_trend"] = self._monthly_trend()
        metrics["top_users"] = self._top_users()
        metrics["maintenance_cost"] = self._maintenance_cost()
        metrics["top_routes"] = self._top_routes()
        metrics["completion_rate"] = self._completion_rate()
        metrics["avg_trips_per_user"] = self._avg_trips_per_user()
        metrics["maintenance_frequency"] = self._maintenance_frequency()
        metrics["trip_outliers"] = self._trip_outliers()
        return metrics

    def build_report_text(self, metrics: Dict[str, object]) -> str:
        timestamp = pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        lines: List[str] = [
            "CityBike Analytics Summary",
            "===========================",
            f"Generated at: {timestamp}",
            "",
        ]

        summary = metrics.get("trip_summary", {})
        lines += [
            "Trip Summary:",
            f"  • Total trips: {summary.get('total_trips', 0):,}",
            f"  • Total distance: {summary.get('total_distance_km', 0.0):.2f} km",
            f"  • Avg duration: {summary.get('avg_duration_minutes', 0.0):.2f} minutes",
            "",
        ]

        lines.append("Top Start Stations:")
        lines.append(self._format_table(metrics["top_stations"].get("start")))
        lines.append("")
        lines.append("Top End Stations:")
        lines.append(self._format_table(metrics["top_stations"].get("end")))
        lines.append("")

        lines.append("Peak Usage Hours:")
        lines.append(self._format_table(metrics["peak_hours"], columns=["hour", "trip_count"]))
        lines.append("")

        lines.append("Weekday Volume:")
        lines.append(self._format_table(metrics["weekday_volume"], columns=["weekday", "trip_count"]))
        lines.append("")

        lines.append("Average Distance by User Type:")
        lines.append(self._format_table(metrics["distance_by_user_type"], columns=["user_type", "avg_distance_km"]))
        lines.append("")

        utilization = metrics.get("bike_utilization")
        lines.append(f"Bike Utilization Rate: {utilization * 100:.2f}%" if utilization is not None else "Bike Utilization Rate: n/a")
        lines.append("")

        lines.append("Monthly Trip Trend:")
        lines.append(self._format_table(metrics["monthly_trend"], columns=["year_month", "trip_count"]))
        lines.append("")

        lines.append("Top 15 Users by Trip Count:")
        lines.append(self._format_table(metrics["top_users"], columns=["user_id", "trip_count"]))
        lines.append("")

        lines.append("Maintenance Cost by Bike Type:")
        lines.append(self._format_table(metrics["maintenance_cost"], columns=["bike_type", "total_cost"]))
        lines.append("")

        lines.append("Most Common Station Pairs:")
        lines.append(self._format_table(metrics["top_routes"], columns=["start_station_id", "end_station_id", "trip_count"]))
        lines.append("")

        completion = metrics.get("completion_rate", {})
        rate = completion.get("completion_rate", 0.0) * 100
        lines.append("Trip Completion Rate:")
        lines.append(f"  • Completed: {completion.get('completed', 0):,}")
        lines.append(f"  • Cancelled: {completion.get('cancelled', 0):,}")
        lines.append(f"  • Completion rate: {rate:.2f}%")
        lines.append("")

        lines.append("Avg Trips per User Type:")
        lines.append(self._format_table(metrics["avg_trips_per_user"], columns=["user_type", "avg_trips_per_user"]))
        lines.append("")

        lines.append("Bikes with Highest Maintenance Frequency:")
        lines.append(self._format_table(metrics["maintenance_frequency"], columns=["bike_id", "maintenance_events"]))
        lines.append("")

        outliers = metrics.get("trip_outliers")
        lines.append("Trip Outliers (top 10 by z-score):")
        lines.append(self._format_table(outliers, columns=["trip_id", "duration_minutes", "distance_km", "max_abs_z"], max_rows=10))

        return "\n".join(lines)

    @staticmethod
    def save_report(report_text: str, report_path: str) -> str:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report_text, encoding="utf-8")
        return str(path)

    @staticmethod
    def _format_table(df: Optional[pd.DataFrame], columns: Optional[List[str]] = None, max_rows: int = 10) -> str:
        if df is None or df.empty:
            return "  (no data)"
        display_df = df.copy()
        if columns:
            display_df = display_df[columns]
        return display_df.head(max_rows).to_string(index=False)

    def _trip_summary(self) -> Dict[str, float]:
        if self.trips.empty:
            return {"total_trips": 0, "total_distance_km": 0.0, "avg_duration_minutes": 0.0}
        return {
            "total_trips": int(len(self.trips)),
            "total_distance_km": float(self.trips["distance_km"].sum()),
            "avg_duration_minutes": float(self.trips["duration_minutes"].mean()),
        }

    def _top_stations(self) -> Dict[str, pd.DataFrame]:
        if self.trips.empty:
            empty = pd.DataFrame(columns=["station_id", "station_name", "trip_count"])
            return {"start": empty, "end": empty}

        lookup = None
        if not self.stations.empty and {"station_id", "station_name"}.issubset(self.stations.columns):
            lookup = self.stations.set_index("station_id")["station_name"]

        def _build(column: str) -> pd.DataFrame:
            counts = (
                self.trips[column]
                .value_counts()
                .reset_index()
                .rename(columns={"index": "station_id", column: "trip_count"})
                .head(10)
            )
            if lookup is not None:
                counts["station_name"] = counts["station_id"].map(lookup)
            else:
                counts["station_name"] = np.nan
            return counts[["station_id", "station_name", "trip_count"]]

        return {"start": _build("start_station_id"), "end": _build("end_station_id")}

    def _peak_hours(self) -> pd.DataFrame:
        if self.trips.empty or "start_time" not in self.trips:
            return pd.DataFrame(columns=["hour", "trip_count"])
        hours = self.trips["start_time"].dt.hour
        return hours.value_counts().sort_index().reset_index().rename(columns={"index": "hour", "start_time": "trip_count"})

    def _weekday_volume(self) -> pd.DataFrame:
        if self.trips.empty or "start_time" not in self.trips:
            return pd.DataFrame(columns=["weekday", "trip_count"])
        weekdays = self.trips["start_time"].dt.day_name()
        ordered = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        counts = weekdays.value_counts().reindex(ordered, fill_value=0)
        return counts.reset_index().rename(columns={"index": "weekday", "start_time": "trip_count"})

    def _distance_by_user_type(self) -> pd.DataFrame:
        if self.trips.empty or "user_type" not in self.trips:
            return pd.DataFrame(columns=["user_type", "avg_distance_km"])
        return self.trips.groupby("user_type")["distance_km"].mean().reset_index(name="avg_distance_km")

    def _bike_utilization(self) -> Optional[float]:
        if self.trips.empty or self.bikes.empty:
            return None
        start = self.trips["start_time"].min()
        end = self.trips["end_time"].max()
        if pd.isna(start) or pd.isna(end) or end <= start:
            return None
        window_minutes = (end - start).total_seconds() / 60
        if window_minutes <= 0:
            return None
        fleet_size = self.bikes["bike_id"].nunique() if "bike_id" in self.bikes else 0
        if fleet_size == 0:
            return None
        utilization = self.trips["duration_minutes"].sum() / (window_minutes * fleet_size)
        return float(min(max(utilization, 0.0), 1.0))

    def _monthly_trend(self) -> pd.DataFrame:
        if self.trips.empty or "start_time" not in self.trips:
            return pd.DataFrame(columns=["year_month", "trip_count"])
        trend = (
            self.trips.assign(year_month=self.trips["start_time"].dt.to_period("M"))
            .groupby("year_month")
            .size()
            .reset_index(name="trip_count")
            .sort_values("year_month")
        )
        trend["year_month"] = trend["year_month"].dt.to_timestamp()
        return trend

    def _top_users(self) -> pd.DataFrame:
        if self.trips.empty or "user_id" not in self.trips:
            return pd.DataFrame(columns=["user_id", "trip_count"])
        return self.trips["user_id"].value_counts().reset_index().head(15).rename(columns={"index": "user_id", "user_id": "trip_count"})

    def _maintenance_cost(self) -> pd.DataFrame:
        if self.maintenance.empty or "bike_type" not in self.maintenance:
            return pd.DataFrame(columns=["bike_type", "total_cost"])
        return self.maintenance.groupby("bike_type")["cost"].sum().reset_index(name="total_cost")

    def _top_routes(self) -> pd.DataFrame:
        required = {"start_station_id", "end_station_id"}
        if self.trips.empty or not required.issubset(self.trips.columns):
            return pd.DataFrame(columns=["start_station_id", "end_station_id", "trip_count"])
        return (
            self.trips.groupby(["start_station_id", "end_station_id"])
            .size()
            .reset_index(name="trip_count")
            .sort_values("trip_count", ascending=False)
            .head(10)
        )

    def _completion_rate(self) -> Dict[str, float]:
        if self.trips.empty or "status" not in self.trips:
            return {"completed": 0, "cancelled": 0, "completion_rate": 0.0}
        counts = self.trips["status"].value_counts()
        completed = int(counts.get("completed", 0))
        cancelled = int(counts.get("cancelled", 0))
        base = completed + cancelled
        rate = (completed / base) if base else 0.0
        return {"completed": completed, "cancelled": cancelled, "completion_rate": rate}

    def _avg_trips_per_user(self) -> pd.DataFrame:
        required = {"user_id", "user_type"}
        if self.trips.empty or not required.issubset(self.trips.columns):
            return pd.DataFrame(columns=["user_type", "avg_trips_per_user"])
        per_user = self.trips.groupby(["user_id", "user_type"]).size().reset_index(name="trip_count")
        return per_user.groupby("user_type")["trip_count"].mean().reset_index(name="avg_trips_per_user")

    def _maintenance_frequency(self) -> pd.DataFrame:
        if self.maintenance.empty or "bike_id" not in self.maintenance:
            return pd.DataFrame(columns=["bike_id", "maintenance_events"])
        return self.maintenance["bike_id"].value_counts().reset_index().rename(columns={"index": "bike_id", "bike_id": "maintenance_events"}).head(10)

    def _trip_outliers(self) -> pd.DataFrame:
        required = {"trip_id", "duration_minutes", "distance_km"}
        if self.trips.empty or not required.issubset(self.trips.columns):
            return pd.DataFrame(columns=["trip_id", "duration_minutes", "distance_km", "max_abs_z"])
        df = self.trips[list(required)].dropna().copy()
        if df.empty:
            return pd.DataFrame(columns=["trip_id", "duration_minutes", "distance_km", "max_abs_z"])
        for column in ("duration_minutes", "distance_km"):
            std = df[column].std(ddof=0)
            if not std or np.isnan(std):
                df[f"{column}_z"] = 0.0
            else:
                df[f"{column}_z"] = (df[column] - df[column].mean()) / std
        df["max_abs_z"] = df[["duration_minutes_z", "distance_km_z"]].abs().max(axis=1)
        return df[df["max_abs_z"] > 3].sort_values("max_abs_z", ascending=False)


