from datetime import datetime


def str_to_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime.date:
    try:
        date_obj = datetime.strptime(date_str, date_format).date()
        return date_obj
    except ValueError as e:
        raise ValueError(f"Invalid date string: {date_str}. Expected format: {date_format}") from e


