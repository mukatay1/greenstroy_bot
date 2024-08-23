from datetime import datetime, time


def get_current_time() -> time:
    return datetime.now().time().replace(microsecond=0)