from datetime import datetime

from config import months_russian


def get_today_month_name() -> str:
    now = datetime.now()
    name_of_month_on_rus = months_russian[now.month]
    return name_of_month_on_rus
