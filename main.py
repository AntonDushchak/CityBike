from loader import load_csv, save_csv
from analyzer import BikeShareSystem

stations_path = "data/stations.csv"
trips_path = "data/trips.csv"
maintenance_path = "data/maintenance.csv"

stations_clean_path = "data/stations_clean.csv"
trips_clean_path = "data/trips_clean.csv"
maintenance_clean_path = "data/maintenance_clean.csv"

def main():
    stations = load_csv(stations_path)
    trips = load_csv(trips_path)
    maintenance = load_csv(maintenance_path)

    save_csv(stations_clean_path, stations)
    save_csv(trips_clean_path, trips)
    save_csv(maintenance_clean_path, maintenance)

    system = BikeShareSystem()

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()