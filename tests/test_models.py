"""Tests for OOP models in models.py."""

from datetime import datetime

import pytest

from models import (
    BIKE_STATUSES,
    BIKE_TYPE_CLASSIC,
    BIKE_TYPE_ELECTRIC,
    BIKE_TYPES,
    MEMBER_TIER_BASIC,
    MEMBER_TIER_PREMIUM,
    MEMBER_TIERS,
    USER_TYPE_CASUAL,
    USER_TYPE_MEMBER,
    Bike,
    CasualUser,
    ClassicBike,
    ElectricBike,
    MaintenanceRecord,
    MemberUser,
    Station,
    Trip,
    User,
)

class TestBike:
    """Tests for Bike class and subclasses."""

    def test_bike_creation_valid(self) -> None:
        """Test creating a bike with valid parameters."""
        bike = Bike(id="BK001", type=BIKE_TYPE_CLASSIC, status="available")
        assert bike.id == "BK001"
        assert bike.type == BIKE_TYPE_CLASSIC
        assert bike.status == "available"

    def test_bike_rejects_invalid_type(self) -> None:
        """Test that Bike rejects invalid bike types."""
        with pytest.raises(ValueError, match="Bike type must be one of"):
            Bike(id="BK001", type="invalid_type", status="available")

    def test_bike_rejects_invalid_status(self) -> None:
        """Test that Bike rejects invalid status values."""
        with pytest.raises(ValueError, match="Bike status must be one of"):
            Bike(id="BK001", type=BIKE_TYPE_CLASSIC, status="broken")

    def test_classic_bike_creation_valid(self) -> None:
        """Test creating a classic bike with valid gear count."""
        bike = ClassicBike(id="BK002", status="available", gear_count=21)
        assert bike.id == "BK002"
        assert bike.type == BIKE_TYPE_CLASSIC
        assert bike.gear_count == 21

    def test_classic_bike_rejects_negative_gears(self) -> None:
        """Test that ClassicBike rejects negative gear count."""
        with pytest.raises(ValueError, match="Gear count must be a positive integer"):
            ClassicBike(id="BK002", status="available", gear_count=-5)

    def test_classic_bike_rejects_zero_gears(self) -> None:
        """Test that ClassicBike rejects zero gear count."""
        with pytest.raises(ValueError, match="Gear count must be a positive integer"):
            ClassicBike(id="BK002", status="available", gear_count=0)

    def test_electric_bike_creation_valid(self) -> None:
        """Test creating an electric bike with valid parameters."""
        bike = ElectricBike(
            id="BK003", status="in_use", battery_level=85.5, max_range_km=40.0
        )
        assert bike.id == "BK003"
        assert bike.type == BIKE_TYPE_ELECTRIC
        assert bike.battery_level == 85.5
        assert bike.max_range_km == 40.0

    def test_electric_bike_rejects_negative_battery(self) -> None:
        """Test that ElectricBike rejects negative battery level."""
        with pytest.raises(ValueError, match="Battery level must be between 0 and 100"):
            ElectricBike(id="BK003", status="available", battery_level=-10, max_range_km=50)

    def test_electric_bike_rejects_battery_over_100(self) -> None:
        """Test that ElectricBike rejects battery level over 100."""
        with pytest.raises(ValueError, match="Battery level must be between 0 and 100"):
            ElectricBike(id="BK003", status="available", battery_level=150, max_range_km=50)

    def test_electric_bike_rejects_negative_range(self) -> None:
        """Test that ElectricBike rejects negative max range."""
        with pytest.raises(ValueError, match="Max range must be non-negative"):
            ElectricBike(id="BK003", status="available", battery_level=100, max_range_km=-10)

    def test_bike_str_representation(self) -> None:
        """Test string representation of Bike."""
        bike = Bike(id="BK001", type=BIKE_TYPE_CLASSIC, status="available")
        assert "BK001" in str(bike)
        assert "classic" in str(bike)

class TestStation:
    """Tests for Station class."""

    def test_station_creation_valid(self) -> None:
        """Test creating a station with valid parameters."""
        station = Station(
            id="ST001", name="Central Station", capacity=25, latitude=48.8, longitude=9.2
        )
        assert station.id == "ST001"
        assert station.name == "Central Station"
        assert station.capacity == 25
        assert station.location == (48.8, 9.2)

    def test_station_rejects_empty_name(self) -> None:
        """Test that Station rejects empty name."""
        with pytest.raises(ValueError, match="Station name must be a non-empty string"):
            Station(id="ST001", name="", capacity=25, latitude=48.8, longitude=9.2)

    def test_station_rejects_negative_capacity(self) -> None:
        """Test that Station rejects negative capacity."""
        with pytest.raises(ValueError, match="Capacity must be a positive integer"):
            Station(id="ST001", name="Test", capacity=-5, latitude=48.8, longitude=9.2)

    def test_station_rejects_invalid_latitude(self) -> None:
        """Test that Station rejects latitude outside valid range."""
        with pytest.raises(ValueError, match="Invalid latitude or longitude"):
            Station(id="ST001", name="Test", capacity=10, latitude=100, longitude=9.2)

    def test_station_rejects_invalid_longitude(self) -> None:
        """Test that Station rejects longitude outside valid range."""
        with pytest.raises(ValueError, match="Invalid latitude or longitude"):
            Station(id="ST001", name="Test", capacity=10, latitude=48.8, longitude=200)

class TestUser:
    """Tests for User class and subclasses."""

    def test_user_creation_valid(self) -> None:
        """Test creating a user with valid parameters."""
        user = User(id="USR001", name="John Doe", email="john@example.com", type=USER_TYPE_CASUAL)
        assert user.id == "USR001"
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.type == USER_TYPE_CASUAL

    def test_user_rejects_invalid_email(self) -> None:
        """Test that User rejects invalid email format."""
        with pytest.raises(ValueError, match="Invalid email address"):
            User(id="USR001", name="John Doe", email="invalid-email", type=USER_TYPE_CASUAL)

    def test_user_rejects_invalid_type(self) -> None:
        """Test that User rejects invalid user type."""
        with pytest.raises(ValueError, match="User type must be one of"):
            User(id="USR001", name="John Doe", email="john@example.com", type="vip")

    def test_casual_user_creation_valid(self) -> None:
        """Test creating a casual user with day passes."""
        user = CasualUser(id="USR002", name="Jane Doe", email="jane@example.com", day_pass_count=3)
        assert user.type == USER_TYPE_CASUAL
        assert user.day_pass_count == 3

    def test_casual_user_rejects_negative_passes(self) -> None:
        """Test that CasualUser rejects negative day pass count."""
        with pytest.raises(ValueError, match="Day pass count must be a non-negative integer"):
            CasualUser(id="USR002", name="Jane", email="jane@example.com", day_pass_count=-1)

    def test_member_user_creation_valid(self) -> None:
        """Test creating a member user with valid tier."""
        start = datetime(2024, 1, 1)
        end = datetime(2025, 1, 1)
        user = MemberUser(
            id="USR003",
            name="Bob Smith",
            email="bob@example.com",
            membership_start_date=start,
            membership_end_date=end,
            tier=MEMBER_TIER_PREMIUM,
        )
        assert user.type == USER_TYPE_MEMBER
        assert user.tier == MEMBER_TIER_PREMIUM
        assert user.membership_start_date == start

    def test_member_user_rejects_invalid_tier(self) -> None:
        """Test that MemberUser rejects invalid membership tier."""
        with pytest.raises(ValueError, match="Tier must be one of"):
            MemberUser(
                id="USR003",
                name="Bob",
                email="bob@example.com",
                membership_start_date=datetime.now(),
                tier="gold",
            )

class TestTrip:
    """Tests for Trip class."""

    @pytest.fixture
    def sample_trip_data(self):
        """Provide sample data for trip tests."""
        user = CasualUser(id="USR001", name="Test User", email="test@example.com")
        bike = ClassicBike(id="BK001", status="in_use", gear_count=21)
        start_station = Station(id="ST001", name="Start", capacity=10, latitude=48.7, longitude=9.1)
        end_station = Station(id="ST002", name="End", capacity=15, latitude=48.8, longitude=9.2)
        return user, bike, start_station, end_station

    def test_trip_creation_valid(self, sample_trip_data) -> None:
        """Test creating a trip with valid parameters."""
        user, bike, start_station, end_station = sample_trip_data
        start_time = datetime(2024, 6, 15, 10, 0)
        end_time = datetime(2024, 6, 15, 10, 30)
        
        trip = Trip(
            id="TR001",
            user=user,
            bike=bike,
            start_station=start_station,
            end_station=end_station,
            start_time=start_time,
            end_time=end_time,
            distance_km=5.5,
        )
        assert trip.id == "TR001"
        assert trip.distance_km == 5.5
        assert trip.user == user

    def test_trip_rejects_negative_distance(self, sample_trip_data) -> None:
        """Test that Trip rejects negative distance."""
        user, bike, start_station, end_station = sample_trip_data
        with pytest.raises(ValueError, match="Distance must be non-negative"):
            Trip(
                id="TR001",
                user=user,
                bike=bike,
                start_station=start_station,
                end_station=end_station,
                start_time=datetime.now(),
                end_time=datetime.now(),
                distance_km=-5.0,
            )

class TestMaintenanceRecord:
    """Tests for MaintenanceRecord class."""

    def test_maintenance_record_creation_valid(self) -> None:
        """Test creating a maintenance record with valid parameters."""
        bike = ClassicBike(id="BK001", status="maintenance", gear_count=21)
        record = MaintenanceRecord(
            id="MR001",
            bike=bike,
            date=datetime(2024, 6, 1),
            maintenance_type="tire_repair",
            cost=25.50,
            description="Replaced front tire",
        )
        assert record.id == "MR001"
        assert record.cost == 25.50
        assert record.bike == bike

    def test_maintenance_record_rejects_negative_cost(self) -> None:
        """Test that MaintenanceRecord rejects negative cost."""
        bike = ClassicBike(id="BK001", status="maintenance", gear_count=21)
        with pytest.raises(ValueError, match="Cost must be non-negative"):
            MaintenanceRecord(
                id="MR001",
                bike=bike,
                date=datetime.now(),
                maintenance_type="repair",
                cost=-50.0,
                description="Test",
            )

    def test_maintenance_record_str_representation(self) -> None:
        """Test string representation of MaintenanceRecord."""
        bike = ClassicBike(id="BK001", status="maintenance", gear_count=21)
        record = MaintenanceRecord(
            id="MR001",
            bike=bike,
            date=datetime(2024, 6, 1),
            maintenance_type="brake_adjustment",
            cost=15.0,
            description="Adjusted brakes",
        )
        assert "MR001" in str(record)
        assert "BK001" in str(record)