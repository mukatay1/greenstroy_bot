from datetime import date, timedelta


def get_previous_day() -> date:
    today = date.today()
    previous_day = today - timedelta(days=1)
    return previous_day