import models
import factories

def dataframe_to_bikes(df, active=True):
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
        
        if active:
            bike.status = "active" if row["status"] == "available" else "in_use"
        else:
            bike.status = "maintenance"
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

def dataframe_to_trips(df):
    """Convert a DataFrame of trip data into a list of Trip objects"""
    trips = []
    for _, row in df.iterrows():
        trip = models.Trip(
            id=row["trip_id"], 
            user_id=row["user_id"], 
            bike_id=row["bike_id"], 
            bike_type=row["bike_type"], 
            start_time=row["start_time"], 
            end_time=row["end_time"], 
            start_station_id=row["start_station_id"], 
            end_station_id=row["end_station_id"], 
            duration_minutes=row["duration_minutes"], 
            distance_km=row["distance_km"], 
            user_type=row["user_type"], 
            status=row["status"])
        trips.append(trip)
    return trips

def dataframe_to_users(df):
    """Convert a DataFrame of trip data into a list of User objects"""
    users = {}
    casual_factory = factories.CasualUserFactory()
    member_factory = factories.MemberUserFactory()
    for _, row in df.iterrows():
        user_id = row["user_id"]
        if user_id not in users:
            if row["user_type"] == "casual":
                user = casual_factory.create_user(
                    id=user_id,
                    name=f"User {user_id}",
                    email=f"user{user_id}@example.com"
                )
            elif row["user_type"] == "member":
                user = member_factory.create_user(
                    id=user_id,
                    name=f"User {user_id}",
                    email=f"user{user_id}@example.com",
                    tier=row.get("tier", "standard")
                )
            else:
                continue
            users[user_id] = user
        else:
            user = users[user_id]
            if row["user_type"] == "casual" and isinstance(user, models.CasualUser):
                user.day_pass_count += 1
    return list(users.values())