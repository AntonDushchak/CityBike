"""
Strategy Pattern: pricing strategies
"""


class PricingStrategy:
    """Base pricing strategy interface"""
    
    def calculate_price(self, duration):
        """Calculate price based on duration"""
        raise NotImplementedError


class StandardPricing(PricingStrategy):
    """Standard pricing strategy"""
    
    def calculate_price(self, duration):
        pass


class PremiumPricing(PricingStrategy):
    """Premium pricing strategy"""
    
    def calculate_price(self, duration):
        pass


class DiscountPricing(PricingStrategy):
    """Discount pricing strategy"""
    
    def calculate_price(self, duration):
        pass
