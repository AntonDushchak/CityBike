"""BikeShareSystem orchestration layer."""

from typing import Dict, Optional

import pandas as pd

from analytics_reporter import AnalyticsReporter
from algorithms import run_algorithm_demo, run_benchmark
from exporter import export_clean_data, export_summary_tables
from loader import load_csv
from utils import (
    clean_data_stations,
    clean_data_trips,
    clean_data_maintenance,
    clean_data_users,
    clean_data_bikes,
)
from visualization import (
    plot_trips_per_station,
    plot_monthly_trip_trend,
    plot_trip_duration_histogram,
    plot_duration_boxplot_by_user_type,
    plot_benchmark_comparison,
)


class BikeShareSystem:
    """Orchestrate loading, cleaning, analysis, reporting, and demos.

    This class provides a unified interface for the complete bike-sharing
    analytics pipeline: loading raw CSV data, cleaning/validating datasets,
    performing analysis, and generating reports and visualizations.

    Attributes:
        stations_path: Path to raw stations CSV file.
        trips_path: Path to raw trips CSV file.
        maintenance_path: Path to raw maintenance CSV file.
        stations: Cleaned stations DataFrame.
        trips: Cleaned trips DataFrame.
        maintenance: Cleaned maintenance DataFrame.
        users: Users DataFrame derived from trips.
        bikes: Bikes DataFrame derived from trips and maintenance.
    """

    def __init__(
        self,
        stations_path: str = "data/stations.csv",
        trips_path: str = "data/trips.csv",
        maintenance_path: str = "data/maintenance.csv",
    ) -> None:
        """Initialize BikeShareSystem with paths to raw data files.

        Args:
            stations_path: Path to stations CSV file.
            trips_path: Path to trips CSV file.
            maintenance_path: Path to maintenance CSV file.
        """
        self.stations_path = stations_path
        self.trips_path = trips_path
        self.maintenance_path = maintenance_path

        self._stations_raw: Optional[pd.DataFrame] = None
        self._trips_raw: Optional[pd.DataFrame] = None
        self._maintenance_raw: Optional[pd.DataFrame] = None

        self.stations: Optional[pd.DataFrame] = None
        self.trips: Optional[pd.DataFrame] = None
        self.maintenance: Optional[pd.DataFrame] = None
        self.users: Optional[pd.DataFrame] = None
        self.bikes: Optional[pd.DataFrame] = None

    def load_data(self) -> "BikeShareSystem":
        """Load raw CSV files into DataFrames.

        Returns:
            Self for method chaining.

        Raises:
            FileNotFoundError: If any CSV file is not found.
        """
        self._stations_raw = load_csv(self.stations_path)
        self._trips_raw = load_csv(self.trips_path)
        self._maintenance_raw = load_csv(self.maintenance_path)
        return self

    def clean_data(self) -> "BikeShareSystem":
        """Clean and validate all loaded datasets.

        Applies data cleaning functions to remove duplicates, invalid entries,
        and standardize formats. Also derives users and bikes DataFrames.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If load_data() has not been called first.
        """
        if self._stations_raw is None or self._trips_raw is None or self._maintenance_raw is None:
            raise ValueError("Raw data not loaded. Call load_data() first.")

        self.stations = clean_data_stations(self._stations_raw)
        self.trips = clean_data_trips(self._trips_raw)
        self.maintenance = clean_data_maintenance(self._maintenance_raw)
        self.users = clean_data_users(self.trips)
        self.bikes = clean_data_bikes(self.trips, self.maintenance)
        return self

    def export_clean_data(
        self,
        stations_path: str = "data/stations_clean.csv",
        trips_path: str = "data/trips_clean.csv",
        maintenance_path: str = "data/maintenance_clean.csv",
    ) -> Dict[str, str]:
        """Export cleaned datasets to CSV files.

        Args:
            stations_path: Output path for cleaned stations.
            trips_path: Output path for cleaned trips.
            maintenance_path: Output path for cleaned maintenance.

        Returns:
            Dictionary mapping dataset names to saved file paths.
        """
        return export_clean_data(
            self.stations,
            self.trips,
            self.maintenance,
            stations_path,
            trips_path,
            maintenance_path,
        )

    def run_pipeline(self) -> Dict[str, object]:
        """Execute the complete analytics pipeline.

        Loads data, cleans it, exports cleaned datasets, generates insights,
        exports summary tables, creates visualizations, and runs benchmarks.

        Returns:
            Dictionary containing all pipeline artifacts and results.
        """
        self.load_data()
        self.clean_data()

        results: Dict[str, object] = {}
        results["clean_exports"] = self.export_clean_data()
        results["insights"] = self.generate_insights()
        results["summary_exports"] = self.export_summary_tables()
        results["figures"] = self.generate_figures()
        results["benchmarks"] = self.benchmark_algorithms()
        results["algorithm_demo"] = self.apply_custom_algorithms()
        return results

    def _reporter(self) -> AnalyticsReporter:
        return AnalyticsReporter(self.users, self.bikes, self.stations, self.trips, self.maintenance)

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
        return export_summary_tables(metrics, output_dir)

    def generate_figures(self) -> list[str]:
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
        return run_algorithm_demo(self.trips, self.stations)

    def benchmark_algorithms(self, sample_size: int = 2000) -> Dict[str, Optional[object]]:
        """Compare custom vs native algorithms using timeit and return artifacts."""
        benchmark_data = run_benchmark(self.trips, sample_size)
        
        if benchmark_data.get("results"):
            figure_path = plot_benchmark_comparison(benchmark_data["results"])
            benchmark_data["figure_path"] = figure_path
        
        return benchmark_data