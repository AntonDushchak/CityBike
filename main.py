"""Entry point: orchestrate the full pipeline from loading to reporting."""

from analyzer import BikeShareSystem

STATIONS_PATH: str = "data/stations.csv"
TRIPS_PATH: str = "data/trips.csv"
MAINTENANCE_PATH: str = "data/maintenance.csv"


def main() -> None:
    """Run the complete CityBike analytics pipeline.

    BikeShareSystem orchestrates:
        1. Loading raw CSV data (stations, trips, maintenance)
        2. Cleaning and validating all datasets
        3. Exporting cleaned data to CSV
        4. Generating analytics report and summary tables
        5. Creating visualizations
        6. Running algorithm benchmarks
    """
    system = BikeShareSystem(
        stations_path=STATIONS_PATH,
        trips_path=TRIPS_PATH,
        maintenance_path=MAINTENANCE_PATH,
    )

    results = system.run_pipeline()
    
    clean_exports = results.get("clean_exports", {})
    if clean_exports:
        print("Cleaned data exports:")
        for label, path in clean_exports.items():
            print(f"  - {label}: {path}")

    insights = results.get("insights", {})
    if insights.get("report_path"):
        print(f"Summary report saved to {insights['report_path']}")

    summary_exports = results.get("summary_exports", {})
    if summary_exports:
        print("Summary CSV exports:")
        for label, path in summary_exports.items():
            print(f"  - {label}: {path}")

    figure_paths = results.get("figures", [])
    if figure_paths:
        print("Saved visualization files:")
        for path in figure_paths:
            print(f"  - {path}")

    benchmarks = results.get("benchmarks", {})
    benchmark_figure = benchmarks.get("figure_path")
    if benchmark_figure:
        print(f"Algorithm benchmark figure saved to {benchmark_figure}")
    elif benchmarks.get("message"):
        print(benchmarks["message"])

    algo_demo = results.get("algorithm_demo", {})
    for message in algo_demo.get("messages", []):
        print(message)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()