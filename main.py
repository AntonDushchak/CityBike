"""Entry point: orchestrate the full pipeline from loading to reporting."""

from loader import load_csv, save_csv
from analyzer import BikeShareSystem
from utils import (
    clean_data_stations,
    clean_data_trips,
    clean_data_maintenance,
    clean_data_users,
    clean_data_bikes,
)

STATIONS_PATH: str = "data/stations.csv"
TRIPS_PATH: str = "data/trips.csv"
MAINTENANCE_PATH: str = "data/maintenance.csv"

STATIONS_CLEAN_PATH: str = "data/stations_clean.csv"
TRIPS_CLEAN_PATH: str = "data/trips_clean.csv"
MAINTENANCE_CLEAN_PATH: str = "data/maintenance_clean.csv"


def main() -> None:
    """Run the complete CityBike analytics pipeline.

    Steps:
        1. Load raw CSV data (stations, trips, maintenance)
        2. Clean and validate all datasets
        3. Export cleaned data to CSV
        4. Generate analytics report and summary tables
        5. Create visualizations
        6. Run algorithm benchmarks
    """
    stations_raw = load_csv(STATIONS_PATH)
    trips_raw = load_csv(TRIPS_PATH)
    maintenance_raw = load_csv(MAINTENANCE_PATH)

    stations_cleaned = clean_data_stations(stations_raw)
    trips_cleaned = clean_data_trips(trips_raw)
    maintenance_cleaned = clean_data_maintenance(maintenance_raw)
    users_cleaned = clean_data_users(trips_cleaned)
    bikes_cleaned = clean_data_bikes(trips_cleaned, maintenance_cleaned)

    save_csv(STATIONS_CLEAN_PATH, stations_cleaned)
    save_csv(TRIPS_CLEAN_PATH, trips_cleaned)
    save_csv(MAINTENANCE_CLEAN_PATH, maintenance_cleaned)

    system = BikeShareSystem(
        users_cleaned,
        bikes_cleaned,
        stations_cleaned,
        trips_cleaned,
        maintenance_cleaned,
    )

    insights = system.generate_insights()
    print(f"Summary report saved to {insights['report_path']}")

    exports = system.export_summary_tables()
    if exports:
        print("Summary CSV exports:")
        for label, path in exports.items():
            print(f"  - {label}: {path}")
    else:
        print("No summary CSV exports generated (missing data).")

    figure_paths = system.generate_figures()
    if figure_paths:
        print("Saved visualization files:")
        for path in figure_paths:
            print(f"  - {path}")
    else:
        print("No visualizations generated (insufficient data).")

    benchmark_artifacts = system.benchmark_algorithms()
    benchmark_figure = benchmark_artifacts.get("figure_path")

    if benchmark_figure:
        print(f"Algorithm benchmark figure saved to {benchmark_figure}")
    else:
        print(benchmark_artifacts.get("message", "Benchmark figure was not generated."))

    algo_results = system.apply_custom_algorithms()
    for message in algo_results.get("messages", []):
        print(message)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()