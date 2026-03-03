"""
Strategy Pattern: pricing strategies
"""

from abc import ABC

class PricingStrategy(ABC):
    """Base pricing strategy interface"""
    
    def calculate_price(self, distance_km):
        pass

class CasualPricing(PricingStrategy):
    """Casual pricing strategy"""
    
    def calculate_price(self, distance_km):
        return 1.0 * distance_km

class PremiumPricing(PricingStrategy):
    """Premium pricing strategy"""
    
    def calculate_price(self, distance_km):
        return 0.8 * distance_km

class PeakHourPricing(PricingStrategy):
    """Peak hour pricing strategy"""
    
    def calculate_price(self, distance_km):
        return 1.5 * distance_km