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

def dataframe_to_maintenance_records(df, bikes):
    """Convert a DataFrame of maintenance data into a list of MaintenanceRecord objects"""
    bikes_dict = {bike.id: bike for bike in bikes}
    records = []
    for _, row in df.iterrows():
        bike = bikes_dict.get(row["bike_id"])
        if bike is None:
            continue
        record = models.MaintenanceRecord(
            id=row["record_id"],
            bike=bike,
            date=row["date"],
            maintenance_type=row["maintenance_type"],
            cost=row["cost"],
            description=row["description"]
        )
        records.append(record)
    return records

def dataframe_to_trips(df, users, bikes, stations):
    """Convert a DataFrame of trip data into a list of Trip objects"""
    users_dict = {user.id: user for user in users}
    bikes_dict = {bike.id: bike for bike in bikes}
    stations_dict = {station.id: station for station in stations}
    
    trips = []
    for _, row in df.iterrows():
        user = users_dict.get(row["user_id"])
        bike = bikes_dict.get(row["bike_id"])
        start_station = stations_dict.get(row["start_station_id"])
        end_station = stations_dict.get(row["end_station_id"])
        
        if None in (user, bike, start_station, end_station):
            continue
            
        trip = models.Trip(
            id=row["trip_id"],
            user=user,
            bike=bike,
            start_station=start_station,
            end_station=end_station,
            start_time=row["start_time"],
            end_time=row["end_time"],
            distance_km=row["distance_km"]
        )
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