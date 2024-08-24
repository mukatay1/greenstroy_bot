from datetime import datetime, timedelta


def get_last_day_of_month() -> datetime:
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)
    return next_month.replace(day=1) - timedelta(days=1)