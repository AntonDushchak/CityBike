"""
Factory Pattern: object creation
"""

from abc import ABC, abstractmethod
from models import Bike, ClassicBike, BIKE_TYPES, BIKE_STATUSES, ElectricBike

class BikeFactory(ABC):
    """Factory for creating bike objects"""
    
    @abstractmethod
    def create_bike(self, id) -> Bike:
        pass

class ClassicBikeFactory(BikeFactory):
    """Factory for creating classic bike objects"""
    
    def create_bike(self, id) -> Bike:
        return ClassicBike(id=id, status="available", gear_count=21)

class ElectricBikeFactory(BikeFactory):
    """Factory for creating electric bike objects"""
    
    def create_bike(self, id) -> Bike:
        return ElectricBike(id=id, status="available", battery_level=100, max_range_km=50) 

# class UserFactory:
#     """Factory for creating user objects"""
    
#     @staticmethod
#     def create_user():
#         """Create a new user instance"""
#         pass
