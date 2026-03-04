from loader import load_csv, save_csv
from analyzer import BikeShareSystem
from utils import clean_data_stations, clean_data_trips, clean_data_maintenance, clean_data_users, clean_data_bikes
from mapper import dataframe_to_stations, dataframe_to_trips, dataframe_to_maintenance_records, dataframe_to_bikes, dataframe_to_users

stations_path = "data/stations.csv"
trips_path = "data/trips.csv"
maintenance_path = "data/maintenance.csv"

stations_clean_path = "data/stations_clean.csv"
trips_clean_path = "data/trips_clean.csv"
maintenance_clean_path = "data/maintenance_clean.csv"



def main():
    stations_raw = load_csv(stations_path)
    trips_raw = load_csv(trips_path)
    maintenance_raw = load_csv(maintenance_path)

    stations_cleaned = clean_data_stations(stations_raw)
    trips_cleaned = clean_data_trips(trips_raw)
    maintenance_cleaned = clean_data_maintenance(maintenance_raw)
    users_cleaned = clean_data_users(trips_cleaned)
    bikes_cleaned = clean_data_bikes(trips_cleaned, maintenance_cleaned)

    save_csv(stations_clean_path, stations_cleaned)
    save_csv(trips_clean_path, trips_cleaned)
    save_csv(maintenance_clean_path, maintenance_cleaned)

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

    algo_results = system.apply_custom_algorithms()
    for message in algo_results.get("messages", []):
        print(message)
    
    # bikes = dataframe_to_bikes(trips_cleaned, active=True)
    # bikes.extend(dataframe_to_bikes(maintenance_cleaned, active=False))
    # users = dataframe_to_users(trips_cleaned)

    # stations = dataframe_to_stations(stations_cleaned)
    # trips = dataframe_to_trips(trips_cleaned, users, bikes, stations)
    # maintenance = dataframe_to_maintenance_records(maintenance_cleaned, bikes)
    
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()