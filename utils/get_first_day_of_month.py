from datetime import datetime


def get_first_day_of_month() -> datetime:
    today = datetime.today()
    return today.replace(day=1)