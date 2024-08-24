from datetime import datetime


def is_weekend(date):
    weekday = date.strftime('%A')
    return weekday in ['Saturday', 'Sunday']

