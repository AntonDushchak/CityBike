"""Domain classes with validation, inheritance, and abstract base class."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional, Tuple

MEMBER_TIER_BASIC: str = "basic"
MEMBER_TIER_PREMIUM: str = "premium"
MEMBER_TIERS: Tuple[str, str] = (MEMBER_TIER_BASIC, MEMBER_TIER_PREMIUM)

BIKE_TYPE_CLASSIC: str = "classic"
BIKE_TYPE_ELECTRIC: str = "electric"
BIKE_TYPES: Tuple[str, str] = (BIKE_TYPE_CLASSIC, BIKE_TYPE_ELECTRIC)

USER_TYPE_CASUAL: str = "casual"
USER_TYPE_MEMBER: str = "member"
USER_TYPES: Tuple[str, str] = (USER_TYPE_CASUAL, USER_TYPE_MEMBER)

BIKE_STATUSES: Tuple[str, str, str] = ("available", "in_use", "maintenance")


class Entity(ABC):
    """Abstract base class for all domain entities.

    Attributes:
        id: Unique identifier for the entity.
        created_at: Timestamp when the entity was created.
    """

    def __init__(self, id: Any) -> None:
        """Initialize an entity with an ID and creation timestamp.

        Args:
            id: Unique identifier for the entity.
        """
        self._id = id
        self._created_at = datetime.now()

    @property
    def id(self) -> Any:
        """Return the entity's unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Return the entity's creation timestamp."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self.__class__.__name__}(id={self.id}, created_at={self.created_at})"

    @abstractmethod
    def __repr__(self) -> str:
        """Return a debug string representation."""
        return self.__str__()


class Bike(Entity):
    """Bike model representing a single bike in the fleet.

    Attributes:
        type: Bike type (classic or electric).
        status: Current status (available, in_use, or maintenance).
    """

    def __init__(self, id: str, type: str, status: str) -> None:
        """Initialize a Bike instance.

        Args:
            id: Unique bike identifier.
            type: One of BIKE_TYPES.
            status: One of BIKE_STATUSES.
        """
        super().__init__(id)
        self.type = type
        self.status = status

    @property
    def type(self) -> str:
        """Return the bike type."""
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """Set the bike type with validation."""
        if value not in BIKE_TYPES:
            raise ValueError(f"Bike type must be one of {BIKE_TYPES}")
        self._type = value

    @property
    def status(self) -> str:
        """Return the bike status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Set the bike status with validation."""
        if value not in BIKE_STATUSES:
            raise ValueError(f"Bike status must be one of {BIKE_STATUSES}")
        self._status = value


class ClassicBike(Bike):
    """Classic bike with gear system.

    Attributes:
        gear_count: Number of gears.
    """

    def __init__(self, id: str, status: str, gear_count: int) -> None:
        """Initialize a ClassicBike instance.

        Args:
            id: Unique bike identifier.
            status: Current bike status.
            gear_count: Number of gears (must be positive).
        """
        super().__init__(id, BIKE_TYPE_CLASSIC, status)
        self.gear_count = gear_count

    @property
    def gear_count(self) -> int:
        """Return the gear count."""
        return self._gear_count

    @gear_count.setter
    def gear_count(self, value: int) -> None:
        """Set the gear count with validation."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Gear count must be a positive integer")
        self._gear_count = value


class ElectricBike(Bike):
    """Electric bike with battery.

    Attributes:
        battery_level: Current battery percentage (0-100).
        max_range_km: Maximum range on full charge in kilometers.
    """

    def __init__(self, id: str, status: str, battery_level: float, max_range_km: float) -> None:
        """Initialize an ElectricBike instance.

        Args:
            id: Unique bike identifier.
            status: Current bike status.
            battery_level: Battery percentage (0-100).
            max_range_km: Maximum range in km.
        """
        super().__init__(id, BIKE_TYPE_ELECTRIC, status)
        self.battery_level = battery_level
        self.max_range_km = max_range_km

    @property
    def battery_level(self) -> float:
        """Return the battery level."""
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value: float) -> None:
        """Set the battery level with validation."""
        if not (0 <= value <= 100):
            raise ValueError("Battery level must be between 0 and 100")
        self._battery_level = value

    @property
    def max_range_km(self) -> float:
        """Return the maximum range."""
        return self._max_range_km

    @max_range_km.setter
    def max_range_km(self, value: float) -> None:
        """Set the maximum range with validation."""
        if value < 0:
            raise ValueError("Max range must be non-negative")
        self._max_range_km = value


class Station(Entity):
    """Docking station for bikes.

    Attributes:
        name: Human-readable station name.
        capacity: Maximum number of bikes the station can hold.
        location: Tuple of (latitude, longitude).
    """

    def __init__(
        self, id: str, name: str, capacity: int, latitude: float, longitude: float
    ) -> None:
        """Initialize a Station instance.

        Args:
            id: Unique station identifier.
            name: Station name.
            capacity: Station capacity.
            latitude: Geographic latitude.
            longitude: Geographic longitude.
        """
        super().__init__(id)
        self.name = name
        self.capacity = capacity
        self.location = (latitude, longitude)

    @property
    def name(self) -> str:
        """Return the station name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the station name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Station name must be a non-empty string")
        self._name = value

    @property
    def capacity(self) -> int:
        """Return the station capacity."""
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        """Set the station capacity with validation."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Capacity must be a positive integer")
        self._capacity = value

    @property
    def location(self) -> Tuple[float, float]:
        """Return the station location as (latitude, longitude)."""
        return self._location

    @location.setter
    def location(self, value: Tuple[float, float]) -> None:
        """Set the station location with coordinate validation."""
        lat, lon = value
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("Invalid latitude or longitude")
        self._location = (lat, lon)

class Trip(Entity):
    """Trip record representing a single bike rental.

    Attributes:
        user: User who took the trip.
        bike: Bike used for the trip.
        start_station: Origin station.
        end_station: Destination station.
        start_time: Trip start timestamp.
        end_time: Trip end timestamp.
        distance_km: Total distance traveled.
    """

    def __init__(
        self,
        id: str,
        user: "User",
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
    ) -> None:
        """Initialize a Trip instance.

        Args:
            id: Unique trip identifier.
            user: User who made the trip.
            bike: Bike used.
            start_station: Starting station.
            end_station: Ending station.
            start_time: When the trip started.
            end_time: When the trip ended.
            distance_km: Distance in kilometers.
        """
        super().__init__(id)
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    @property
    def distance_km(self) -> float:
        """Return the trip distance in kilometers."""
        return self._distance_km

    @distance_km.setter
    def distance_km(self, value: float) -> None:
        """Set the trip distance with validation."""
        if value < 0:
            raise ValueError("Distance must be non-negative")
        self._distance_km = value


class User(Entity):
    """Base user class for bike-share customers.

    Attributes:
        name: User's full name.
        email: User's email address.
        type: User type (casual or member).
    """

    def __init__(self, id: str, name: str, email: str, type: str) -> None:
        """Initialize a User instance.

        Args:
            id: Unique user identifier.
            name: User's name.
            email: User's email address.
            type: One of USER_TYPES.
        """
        super().__init__(id)
        self.name = name
        self.email = email
        self.type = type

    @property
    def name(self) -> str:
        """Return the user's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the user's name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("User name must be a non-empty string")
        self._name = value

    @property
    def email(self) -> str:
        """Return the user's email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set the user's email with validation."""
        if "@" not in value or not isinstance(value, str):
            raise ValueError("Invalid email address")
        self._email = value

    @property
    def type(self) -> str:
        """Return the user type."""
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """Set the user type with validation."""
        if value not in USER_TYPES:
            raise ValueError(f"User type must be one of {USER_TYPES}")
        self._type = value


class CasualUser(User):
    """Casual user with pay-per-ride access.

    Attributes:
        day_pass_count: Number of day passes purchased.
    """

    def __init__(self, id: str, name: str, email: str, day_pass_count: int = 0) -> None:
        """Initialize a CasualUser instance.

        Args:
            id: Unique user identifier.
            name: User's name.
            email: User's email.
            day_pass_count: Number of day passes (default 0).
        """
        super().__init__(id, name, email, USER_TYPE_CASUAL)
        self.day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        """Return the number of day passes."""
        return self._day_pass_count

    @day_pass_count.setter
    def day_pass_count(self, value: int) -> None:
        """Set the day pass count with validation."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Day pass count must be a non-negative integer")
        self._day_pass_count = value


class MemberUser(User):
    """Member user with subscription access.

    Attributes:
        membership_start_date: When membership began.
        membership_end_date: When membership expires.
        tier: Membership tier (basic or premium).
    """

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        membership_start_date: datetime,
        tier: str,
        membership_end_date: Optional[datetime] = None,
    ) -> None:
        """Initialize a MemberUser instance.

        Args:
            id: Unique user identifier.
            name: User's name.
            email: User's email.
            membership_start_date: Start date of membership.
            tier: Membership tier.
            membership_end_date: Optional end date.
        """
        super().__init__(id, name, email, USER_TYPE_MEMBER)
        self.membership_start_date = membership_start_date
        self.membership_end_date = membership_end_date
        self.tier = tier

    @property
    def tier(self) -> str:
        """Return the membership tier."""
        return self._tier

    @tier.setter
    def tier(self, value: str) -> None:
        """Set the membership tier with validation."""
        if value not in MEMBER_TIERS:
            raise ValueError(f"Tier must be one of {MEMBER_TIERS}")
        self._tier = value


class MaintenanceRecord:
    """Maintenance event for a bike.

    Attributes:
        id: Unique record identifier.
        bike: Bike that was serviced.
        date: Date of maintenance.
        maintenance_type: Type of service performed.
        cost: Cost of maintenance.
        description: Details about the work done.
    """

    def __init__(
        self,
        id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str,
    ) -> None:
        """Initialize a MaintenanceRecord instance.

        Args:
            id: Unique record identifier.
            bike: Bike that was maintained.
            date: Date of maintenance.
            maintenance_type: Type of maintenance.
            cost: Cost in currency units.
            description: Description of work.
        """
        self.id = id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    @property
    def cost(self) -> float:
        """Return the maintenance cost."""
        return self._cost

    @cost.setter
    def cost(self, value: float) -> None:
        """Set the cost with validation."""
        if value < 0:
            raise ValueError("Cost must be non-negative")
        self._cost = value

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"MaintenanceRecord(id={self.id}, bike_id={self.bike.id}, date={self.date}, type={self.maintenance_type}, cost={self.cost})"

    def __repr__(self) -> str:
        """Return a debug string representation."""
        return self.__str__()
