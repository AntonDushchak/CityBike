"""
BikeShareSystem: analysis methods
"""

import pandas as pd

from CityBike.analytics_reporter import AnalyticsReporter

class BikeShareSystem:
    """Orchestrate loading, cleaning, analysis, and reporting."""

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