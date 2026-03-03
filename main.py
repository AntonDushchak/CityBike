from loader import load_csv, save_csv
from analyzer import BikeShareSystem
from utils import clean_data_stations, clean_data_trips, clean_data_maintenance
from mapper import dataframe_to_stations, dataframe_to_trips, dataframe_to_maintenance_records, dataframe_to_bikes

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

    save_csv(stations_clean_path, stations_cleaned)
    save_csv(trips_clean_path, trips_cleaned)
    save_csv(maintenance_clean_path, maintenance_cleaned)

    stations = dataframe_to_stations(stations_cleaned)
    trips = dataframe_to_trips(trips_cleaned)
    maintenance = dataframe_to_maintenance(maintenance_cleaned)

    system = BikeShareSystem()

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()