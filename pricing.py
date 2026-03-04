"""Strategy Pattern: interchangeable pricing strategies for trip cost calculation."""

from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Abstract base class for pricing strategies."""

    @abstractmethod
    def calculate_price(self, distance_km: float) -> float:
        """Calculate trip price based on distance.

        Args:
            distance_km: Trip distance in kilometers.

        Returns:
            Calculated price.
        """
        pass

class CasualPricing(PricingStrategy):
    """Standard pricing strategy for casual users."""

    def calculate_price(self, distance_km: float) -> float:
        """Calculate price at $1.00 per km.

        Args:
            distance_km: Trip distance in kilometers.

        Returns:
            Calculated price.
        """
        return 1.0 * distance_km

class MemberPricing(PricingStrategy):
    """Discounted pricing strategy for member users."""

    def calculate_price(self, distance_km: float) -> float:
        """Calculate price at $0.80 per km (20% discount).

        Args:
            distance_km: Trip distance in kilometers.

        Returns:
            Calculated price.
        """
        return 0.8 * distance_km

class PeakHourPricing(PricingStrategy):
    """Surge pricing strategy for peak hours."""

    def calculate_price(self, distance_km: float) -> float:
        """Calculate price at $1.50 per km (50% surcharge).

        Args:
            distance_km: Trip distance in kilometers.

        Returns:
            Calculated price.
        """
        return 1.5 * distance_km