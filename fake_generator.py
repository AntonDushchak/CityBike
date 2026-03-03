import datetime
from random import random

def generate_fake_start_and_end_date():
    """Generate random start and end dates for trips"""
    start_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))
    end_date = start_date + datetime.timedelta(minutes=random.randint(5, 120))
    return start_date, end_date
