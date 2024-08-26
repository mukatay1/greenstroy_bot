from datetime import datetime, timedelta


def calculate_hours(arrival_time, departure_time=None, extra_time='00:00'):
    if arrival_time:
        if not departure_time and extra_time == '00:00':
            return '00:00'

        arrival = datetime.strptime(arrival_time, '%H:%M')

        if not departure_time or departure_time == '00:00':
            midnight = datetime.combine(arrival.date(), datetime.min.time()) + timedelta(days=1)
            duration = midnight - arrival
        else:
            departure = datetime.strptime(departure_time, '%H:%M')
            duration = departure - arrival

        extra_duration = timedelta(hours=int(extra_time.split(':')[0]), minutes=int(extra_time.split(':')[1]))
        total_duration = duration + extra_duration
        hours = total_duration.seconds // 3600
        minutes = (total_duration.seconds % 3600) // 60

        return f'{hours:02}:{minutes:02}'

    return '00:00'