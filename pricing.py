"""
Strategy Pattern: pricing strategies
"""

from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Base pricing strategy interface"""
    
    @abstractmethod
    def calculate_price(self, distance_km: float) -> float:
        """Calculate trip price based on distance"""
        pass

class CasualPricing(PricingStrategy):
    """Casual pricing strategy"""
    
    def calculate_price(self, distance_km: float) -> float:
        return 1.0 * distance_km

class PremiumPricing(PricingStrategy):
    """Premium pricing strategy"""
    
    def calculate_price(self, distance_km: float) -> float:
        return 0.8 * distance_km

class PeakHourPricing(PricingStrategy):
    """Peak hour pricing strategy"""
    
    def calculate_price(self, distance_km: float) -> float:
        return 1.5 * distance_km