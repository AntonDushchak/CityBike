"""Utilities for generating fake test data."""

import datetime
import random
from typing import Tuple


def generate_fake_start_and_end_date() -> Tuple[datetime.datetime, datetime.datetime]:
    """Generate random start and end dates for membership or trips.

    Returns:
        Tuple of (start_date, end_date) where end is 5-120 minutes after start.
    """
    start_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))
    end_date = start_date + datetime.timedelta(minutes=random.randint(5, 120))
    return start_date, end_date
