"""
Factory Pattern: object creation
"""

from abc import ABC, abstractmethod
from models import Bike, ClassicBike, ElectricBike, User, CasualUser, MemberUser, BIKE_TYPES, BIKE_STATUSES, MEMBER_TIERS
from fake_generator import generate_fake_start_and_end_date

class BikeFactory(ABC):
    """Factory for creating bike objects"""
    
    @abstractmethod
    def create_bike(self, id) -> Bike:
        pass

class ClassicBikeFactory(BikeFactory):
    """Factory for creating classic bike objects"""
    
    def create_bike(self, id, gear_count=21) -> Bike:
        return ClassicBike(id=id, status="available", gear_count=gear_count)

class ElectricBikeFactory(BikeFactory):
    """Factory for creating electric bike objects"""
    
    def create_bike(self, id, battery_level=100, max_range_km=50) -> Bike:
        return ElectricBike(id=id, status="available", battery_level=battery_level, max_range_km=max_range_km) 

class UserFactory(ABC):
    """Factory for creating user objects"""
    
    @abstractmethod
    def create_user(self, id, name, email, type) -> User:
        pass

class CasualUserFactory(UserFactory):
    """Factory for creating casual user objects"""
    
    def create_user(self, id, name, email) -> User:
        return CasualUser(id=id, name=name, email=email)
    
class MemberUserFactory(UserFactory):
    """Factory for creating member user objects"""
    
    def create_user(self, id, name, email, tier="standard") -> User:
        start_date, end_date = generate_fake_start_and_end_date()
        return MemberUser(id=id, name=name, email=email, membership_start_date=start_date, membership_end_date=end_date, tier=tier)