import models
import factories

def dataframe_to_bikes(df, status):
    """Convert a DataFrame of bike data into a list of Bike objects"""
    bikes = []
    classic_factory = factories.ClassicBikeFactory()
    electric_factory = factories.ElectricBikeFactory()
    for _, row in df.iterrows():
        if row["bike_type"] == "classic":
            bike = classic_factory.create_bike(row["bike_id"])
        elif row["bike_type"] == "electric":
            bike = electric_factory.create_bike(row["bike_id"])
        else:
            continue
        bike.status = status
        bikes.append(bike)
    return bikes

def dataframe_to_stations(df):
    """Convert a DataFrame of station data into a list of Station objects"""
    stations = []
    for _, row in df.iterrows():
        station = models.Station(
            id=row["station_id"], 
            name=row["station_name"], 
            capacity=row["capacity"], 
            latitude=row["latitude"], 
            longitude=row["longitude"])
        stations.append(station)
    return stations

def dataframe_to_maintenance_records(df):
    """Convert a DataFrame of maintenance data into a list of MaintenanceRecord objects"""
    records = []
    for _, row in df.iterrows():
        record = models.MaintenanceRecord(
            id=row["record_id"], 
            bike_id=row["bike_id"], 
            bike_type=row["bike_type"], 
            date=row["date"], 
            maintenance_type=row["maintenance_type"], 
            cost=row["cost"], 
            description=row["description"])
        records.append(record)
    return records