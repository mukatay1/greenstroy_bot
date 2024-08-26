from datetime import datetime, timedelta, time


def calculate_extra_hours(arrival_time, departure_time=None, extra_time='00:00'):
    if arrival_time:
        arrival = datetime.strptime(arrival_time, '%H:%M')

        if not departure_time and extra_time != '00:00':
            extra_duration = timedelta(hours=int(extra_time.split(':')[0]), minutes=int(extra_time.split(':')[1]))
            total_duration = extra_duration + timedelta(hours=3)

        else:
            evening_cutoff = datetime.combine(arrival.date(), time(21, 0))
            duration = timedelta()

            if departure_time:
                departure = datetime.strptime(departure_time, '%H:%M')
                if arrival.time() > time(21, 0):
                    duration = datetime.combine(arrival.date(), departure.time()) - datetime.combine(arrival.date(), arrival.time())
                elif arrival.time() <= time(21, 0):
                    if departure.time() > time(21, 0):
                        duration = datetime.combine(arrival.date(), departure.time()) - evening_cutoff
                    else:
                        duration = datetime.combine(arrival.date(), departure.time()) - datetime.combine(arrival.date(), arrival.time())
            else:
                if arrival.time() > time(21, 0):
                    duration = timedelta()

            extra_duration = timedelta(hours=int(extra_time.split(':')[0]), minutes=int(extra_time.split(':')[1]))
            total_duration = duration + extra_duration

        hours = total_duration.seconds // 3600
        minutes = (total_duration.seconds % 3600) // 60

        return f'{hours:02}:{minutes:02}'

    return '00:00'
