from datetime import datetime


def calculate_hours(arrival_time, departure_time):
    if arrival_time and departure_time:
        arrival = datetime.strptime(arrival_time, '%H:%M')
        departure = datetime.strptime(departure_time, '%H:%M')
        duration = departure - arrival
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f'{hours:02}:{minutes:02}'
    return '00:00'