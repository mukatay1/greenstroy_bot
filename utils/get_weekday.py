from config import weekdays


def get_weekday(date):
    weekdays_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_en = date.strftime('%A')
    return weekdays[weekdays_en.index(weekday_en)]