"""BikeShareSystem orchestration layer."""

from pathlib import Path
from timeit import timeit
from typing import Dict, List, Optional

import pandas as pd

from analytics_reporter import AnalyticsReporter
from algorithms import my_sort, python_sort, my_search, pandas_search
from loader import save_csv
from visualization import (
    plot_trips_per_station,
    plot_monthly_trip_trend,
    plot_trip_duration_histogram,
    plot_duration_boxplot_by_user_type,
    plot_benchmark_comparison,
)

TRIP_PREVIEW_COUNT = 5
STATION_SAMPLE_INDEX = 0
BENCHMARK_SAMPLE_SIZE = 2000
BENCHMARK_SORT_RUNS = 5
BENCHMARK_SEARCH_RUNS = 250

class BikeShareSystem:
    """Orchestrate loading, cleaning, analysis, reporting, and demos."""

    def __init__(self, users_df, bikes_df, stations_df, trips_df, maintenance_df):
        self.users = users_df
        self.bikes = bikes_df
        self.stations = stations_df
        self.trips = trips_df
        self.maintenance = maintenance_df

    def _reporter(self) -> AnalyticsReporter:
        return AnalyticsReporter(self.users, self.bikes, self.stations, self.trips, self.maintenance)

    def analyze_trips(self):
        reporter = self._reporter()
        metrics = reporter.compute_metrics()
        keys = [
            "trip_summary",
            "top_stations",
            "peak_hours",
            "weekday_volume",
            "distance_by_user_type",
            "bike_utilization",
            "monthly_trend",
            "top_users",
            "top_routes",
            "completion_rate",
            "avg_trips_per_user",
            "trip_outliers",
        ]
        return {key: metrics[key] for key in keys}

    def analyze_stations(self):
        reporter = self._reporter()
        metrics = reporter.compute_metrics()
        keys = ["top_stations", "peak_hours", "weekday_volume", "top_routes"]
        return {key: metrics[key] for key in keys}

    def analyze_users(self):
        reporter = self._reporter()
        metrics = reporter.compute_metrics()
        keys = ["top_users", "distance_by_user_type", "avg_trips_per_user"]
        return {key: metrics[key] for key in keys}

    def analyze_maintenance(self):
        reporter = self._reporter()
        metrics = reporter.compute_metrics()
        keys = ["maintenance_cost", "maintenance_frequency"]
        return {key: metrics[key] for key in keys}

    def generate_insights(self, report_path: str = "output/summary_report.txt"):
        reporter = self._reporter()
        metrics = reporter.compute_metrics()
        report_text = reporter.build_report_text(metrics)
        saved_path = reporter.save_report(report_text, report_path)
        return {"report_path": saved_path, "metrics": metrics}

    def export_summary_tables(self, output_dir: str = "output") -> Dict[str, str]:
        """Export top stations, top users, and maintenance summaries to CSV."""

        reporter = self._reporter()
        metrics = reporter.compute_metrics()
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        exports: Dict[str, str] = {}

        # Top stations (start + end combined with role flag)
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

        # Top users
        top_users = metrics.get("top_users")
        if isinstance(top_users, pd.DataFrame) and not top_users.empty:
            users_path = out_dir / "top_users.csv"
            save_csv(str(users_path), top_users)
            exports["top_users"] = str(users_path)

        # Maintenance summaries (cost + frequency)
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

    def generate_figures(self) -> List[str]:
        """Produce the required Matplotlib charts and return saved paths."""

        figure_paths = [
            plot_trips_per_station(self.trips, self.stations),
            plot_monthly_trip_trend(self.trips),
            plot_trip_duration_histogram(self.trips),
            plot_duration_boxplot_by_user_type(self.trips),
        ]
        return [path for path in figure_paths if path]

    def apply_custom_algorithms(self) -> Dict[str, object]:
        """Run my_sort/my_search on real trip and station data."""

        result: Dict[str, object] = {
            "trip_sort_ids": None,
            "trip_search": None,
            "station_search": None,
            "messages": [],
        }

        if self.trips is not None and not self.trips.empty and "trip_id" in self.trips:
            trip_columns = [
                col
                for col in ["trip_id", "start_station_id", "duration_minutes", "distance_km", "user_type"]
                if col in self.trips
            ]
            trip_records = self.trips[trip_columns].to_dict("records")
            if trip_records:
                sort_key_trip = lambda row: row["trip_id"]
                sorted_trips = my_sort(trip_records, key=sort_key_trip)
                result["trip_sort_ids"] = [row["trip_id"] for row in sorted_trips[:TRIP_PREVIEW_COUNT]]
                target_trip = sorted_trips[len(sorted_trips) // 2]
                trip_index = my_search(sorted_trips, target_trip, key=sort_key_trip)
                result["trip_search"] = {
                    "trip_id": target_trip["trip_id"],
                    "index": trip_index,
                }
            else:
                result["messages"].append("Trip dataset empty after conversion; custom algorithms skipped.")
        else:
            result["messages"].append("Trip data unavailable for custom algorithm demo.")

        if self.stations is not None and not self.stations.empty and "station_id" in self.stations:
            station_columns = [col for col in ["station_id", "station_name", "capacity"] if col in self.stations]
            station_records = self.stations[station_columns].to_dict("records")
            if station_records:
                sort_key_station = lambda row: row["station_id"]
                sorted_stations = my_sort(station_records, key=sort_key_station)
                target_station = sorted_stations[STATION_SAMPLE_INDEX]
                station_index = my_search(sorted_stations, target_station, key=sort_key_station)
                result["station_search"] = {
                    "station_id": target_station["station_id"],
                    "station_name": target_station.get("station_name"),
                    "index": station_index,
                }
            else:
                result["messages"].append("Station dataset empty after conversion; station search skipped.")
        else:
            result["messages"].append("Station data unavailable for custom algorithm demo.")

        return result

    def benchmark_algorithms(self, sample_size: int = BENCHMARK_SAMPLE_SIZE) -> Dict[str, Optional[object]]:
        """Compare custom vs native algorithms using timeit and return artifacts."""

        if self.trips is None or self.trips.empty or "trip_id" not in self.trips:
            return {"results": None, "figure_path": None, "message": "Missing trip data for benchmarks."}

        subset_columns = [
            col for col in ["trip_id", "duration_minutes", "distance_km", "user_type"] if col in self.trips
        ]
        trip_sample = self.trips[subset_columns].head(sample_size).to_dict("records")
        if not trip_sample:
            return {"results": None, "figure_path": None, "message": "Insufficient trip sample for benchmarks."}

        sort_key = lambda row: row["trip_id"]
        my_sort_time = timeit(lambda: my_sort(trip_sample, sort_key), number=BENCHMARK_SORT_RUNS)
        python_sort_time = timeit(lambda: python_sort(trip_sample, sort_key), number=BENCHMARK_SORT_RUNS)

        sorted_sample = python_sort(trip_sample, sort_key)
        if not sorted_sample:
            return {"results": None, "figure_path": None, "message": "Sorted sample empty; benchmarks aborted."}

        target = sorted_sample[len(sorted_sample) // 2]
        my_search_time = timeit(lambda: my_search(sorted_sample, target, sort_key), number=BENCHMARK_SEARCH_RUNS)
        pandas_search_time = timeit(lambda: pandas_search(sorted_sample, target, sort_key), number=BENCHMARK_SEARCH_RUNS)

        benchmark_results = {
            "my_sort": my_sort_time / BENCHMARK_SORT_RUNS,
            "python_sort": python_sort_time / BENCHMARK_SORT_RUNS,
            "my_search": my_search_time / BENCHMARK_SEARCH_RUNS,
            "pandas_search": pandas_search_time / BENCHMARK_SEARCH_RUNS,
        }

        figure_path = plot_benchmark_comparison(benchmark_results)
        return {"results": benchmark_results, "figure_path": figure_path, "message": None}