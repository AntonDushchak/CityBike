"""Factory Pattern: object creation from raw data."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Tuple

from fake_generator import generate_fake_start_and_end_date
from models import (
    Bike,
    CasualUser,
    ClassicBike,
    ElectricBike,
    MemberUser,
    User,
    MEMBER_TIERS,
)


class BikeFactory(ABC):
    """Abstract factory for creating Bike objects."""

    @abstractmethod
    def create_bike(self, id: str) -> Bike:
        """Create a Bike instance.

        Args:
            id: Unique bike identifier.

        Returns:
            New Bike instance.
        """
        pass


class ClassicBikeFactory(BikeFactory):
    """Factory for creating ClassicBike objects."""

    def create_bike(self, id: str, gear_count: int = 21) -> ClassicBike:
        """Create a ClassicBike instance.

        Args:
            id: Unique bike identifier.
            gear_count: Number of gears (default 21).

        Returns:
            New ClassicBike instance.
        """
        return ClassicBike(id=id, status="available", gear_count=gear_count)


class ElectricBikeFactory(BikeFactory):
    """Factory for creating ElectricBike objects."""

    def create_bike(
        self, id: str, battery_level: float = 100, max_range_km: float = 50
    ) -> ElectricBike:
        """Create an ElectricBike instance.

        Args:
            id: Unique bike identifier.
            battery_level: Initial battery level (default 100).
            max_range_km: Maximum range in km (default 50).

        Returns:
            New ElectricBike instance.
        """
        return ElectricBike(
            id=id, status="available", battery_level=battery_level, max_range_km=max_range_km
        )


class UserFactory(ABC):
    """Abstract factory for creating User objects."""

    @abstractmethod
    def create_user(self, id: str, name: str, email: str) -> User:
        """Create a User instance.

        Args:
            id: Unique user identifier.
            name: User's name.
            email: User's email address.

        Returns:
            New User instance.
        """
        pass


class CasualUserFactory(UserFactory):
    """Factory for creating CasualUser objects."""

    def create_user(self, id: str, name: str, email: str) -> CasualUser:
        """Create a CasualUser instance.

        Args:
            id: Unique user identifier.
            name: User's name.
            email: User's email address.

        Returns:
            New CasualUser instance.
        """
        return CasualUser(id=id, name=name, email=email)


class MemberUserFactory(UserFactory):
    """Factory for creating MemberUser objects."""

    def create_user(
        self, id: str, name: str, email: str, tier: str = "basic"
    ) -> MemberUser:
        """Create a MemberUser instance.

        Args:
            id: Unique user identifier.
            name: User's name.
            email: User's email address.
            tier: Membership tier (default 'basic').

        Returns:
            New MemberUser instance.
        """
        start_date, end_date = generate_fake_start_and_end_date()
        return MemberUser(
            id=id,
            name=name,
            email=email,
            membership_start_date=start_date,
            membership_end_date=end_date,
            tier=tier,
        )