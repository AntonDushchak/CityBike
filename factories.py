"""
Factory Pattern: object creation
"""

from models import Bike, Station, Trip, User


class BikeFactory:
    """Factory for creating bike objects"""
    
    @staticmethod
    def create_bike():
        """Create a new bike instance"""
        pass


class StationFactory:
    """Factory for creating station objects"""
    
    @staticmethod
    def create_station():
        """Create a new station instance"""
        pass


class TripFactory:
    """Factory for creating trip objects"""
    
    @staticmethod
    def create_trip():
        """Create a new trip instance"""
        pass


class UserFactory:
    """Factory for creating user objects"""
    
    @staticmethod
    def create_user():
        """Create a new user instance"""
        pass
