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
    
    def create_bike(self, id, gear_count=21) -> Bike:
        return ClassicBike(id=id, status="available", gear_count=gear_count)

class ElectricBikeFactory(BikeFactory):
    """Factory for creating electric bike objects"""
    
    def create_bike(self, id, battery_level=100, max_range_km=50) -> Bike:
        return ElectricBike(id=id, status="available", battery_level=battery_level, max_range_km=max_range_km) 

# class UserFactory:
#     """Factory for creating user objects"""
    
#     @staticmethod
#     def create_user():
#         pass
