"""
OOP classes (Entity, Bike, Station, ...)
"""
from abc import ABC, abstractmethod
from datetime import datetime

MEMBER_TIER_BASIC = "basic"
MEMBER_TIER_PREMIUM = "premium"
MEMBER_TIERS = (MEMBER_TIER_BASIC, MEMBER_TIER_PREMIUM)

BIKE_TYPE_CLASSIC = "classic"
BIKE_TYPE_ELECTRIC = "electric"
BIKE_TYPES = (BIKE_TYPE_CLASSIC, BIKE_TYPE_ELECTRIC)

USER_TYPE_CASUAL = "casual"
USER_TYPE_MEMBER = "member"
USER_TYPES = (USER_TYPE_CASUAL, USER_TYPE_MEMBER)

BIKE_STATUSES = ("available", "in_use", "maintenance")

class Entity(ABC):
    """Base entity class"""

    def __init__(self, id):
        self._id = id
        self._created_at = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @abstractmethod
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, created_at={self.created_at})"
    
    @abstractmethod
    def __repr__(self):
        return self.__str__()

class Bike(Entity):
    """Bike model class"""
    def __init__(self, id, type, status):
        super().__init__(id)
        self.type = type
        self.status = status

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in BIKE_TYPES:
            raise ValueError(f"Bike type must be one of {BIKE_TYPES}")
        self._type = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in BIKE_STATUSES:
            raise ValueError(f"Bike status must be one of {BIKE_STATUSES}")
        self._status = value

class ClassicBike(Bike):
    """Classic bike model class"""
    def __init__(self, id, status, gear_count):
        super().__init__(id, BIKE_TYPE_CLASSIC, status)
        self.gear_count = gear_count

    @property
    def gear_count(self):
        return self._gear_count

    @gear_count.setter
    def gear_count(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Gear count must be a positive integer")
        self._gear_count = value

class ElectricBike(Bike):
    """Electric bike model class"""
    def __init__(self, id, status, battery_level, max_range_km):
        super().__init__(id, BIKE_TYPE_ELECTRIC, status)
        self.battery_level = battery_level
        self.max_range_km = max_range_km

    @property
    def battery_level(self):
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value):
        if not (0 <= value <= 100):
            raise ValueError("Battery level must be between 0 and 100")
        self._battery_level = value

    @property
    def max_range_km(self):
        return self._max_range_km

    @max_range_km.setter
    def max_range_km(self, value):
        if value < 0:
            raise ValueError("Max range must be non-negative")
        self._max_range_km = value

class Station(Entity):
    """Station model class"""
    def __init__(self, id, name, capacity, latitude, longitude):
        super().__init__(id)
        self.name = name
        self.capacity = capacity
        self.location = (latitude, longitude)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Station name must be a non-empty string")
        self._name = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Capacity must be a positive integer")
        self._capacity = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        lat, lon = value
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("Invalid latitude or longitude")
        self._location = (lat, lon)

class Trip(Entity):
    """Trip model class"""
    def __init__(self, id, user, bike, start_station, end_station, start_time, end_time, distance_km):
        super().__init__(id)
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    @property
    def distance_km(self):
        return self._distance_km

    @distance_km.setter
    def distance_km(self, value):
        if value < 0:
            raise ValueError("Distance must be non-negative")
        self._distance_km = value

class User(Entity):
    """User model class"""
    def __init__(self, id, name, email, type):
        super().__init__(id)
        self.name = name
        self.email = email
        self.type = type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("User name must be a non-empty string")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or not isinstance(value, str):
            raise ValueError("Invalid email address")
        self._email = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in USER_TYPES:
            raise ValueError(f"User type must be one of {USER_TYPES}")
        self._type = value

class CasualUser(User):
    """Casual user model class"""
    def __init__(self, id, name, email, day_pass_count = 0):
        super().__init__(id, name, email, USER_TYPE_CASUAL)
        self.day_pass_count = day_pass_count

    @property
    def day_pass_count(self):
        return self._day_pass_count

    @day_pass_count.setter
    def day_pass_count(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Day pass count must be a non-negative integer")
        self._day_pass_count = value

class MemberUser(User):
    """Member user model class"""
    def __init__(self, id, name, email, membership_start_date, tier, membership_end_date=None):
        super().__init__(id, name, email, USER_TYPE_MEMBER)
        self.membership_start_date = membership_start_date
        self.membership_end_date = membership_end_date
        self.tier = tier

    @property
    def tier(self):
        return self._tier

    @tier.setter
    def tier(self, value):
        if value not in MEMBER_TIERS:
            raise ValueError(f"Tier must be one of {MEMBER_TIERS}")
        self._tier = value

class MaintenanceRecord:
    """Maintenance record model class"""
    def __init__(self, id, bike, date, maintenance_type, cost, description):
        self.id = id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if value < 0:
            raise ValueError("Cost must be non-negative")
        self._cost = value

    def __str__(self):
        return f"MaintenanceRecord(id={self.id}, bike_id={self.bike.id}, date={self.date}, type={self.maintenance_type}, cost={self.cost})"
    
    def __repr__(self):
        return self.__str__()
