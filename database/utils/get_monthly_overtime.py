from datetime import datetime, timedelta, time

from database.main import SessionLocal
from database.models.models import Attendance
from utils.calculate_extra_hours import calculate_extra_hours
from utils.calculate_hours import calculate_hours


def get_monthly_overtime(employee_id: int) -> str:
    with SessionLocal() as db:
        now = datetime.now()
        year = now.year
        month = now.month

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)

        attendances = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).all()
        total_overtime = timedelta()
        for attendance in attendances:
            is_weekend = attendance.date.weekday() >= 5

            if not is_weekend:
                arrival_time = attendance.arrival_time.strftime('%H:%M') if attendance.arrival_time else ''
                departure_time = attendance.departure_time.strftime('%H:%M') if attendance.departure_time else ''
                extra_time = attendance.overtime.strftime('%H:%M') if attendance.overtime else '00:00'
                overtime_str = calculate_extra_hours(arrival_time, departure_time, extra_time)
                overtime_hours, overtime_minutes = map(int, overtime_str.split(':'))
                overtime = timedelta(hours=overtime_hours, minutes=overtime_minutes)
            else:
                arrival_time = attendance.arrival_time.strftime('%H:%M') if attendance.arrival_time else ''
                departure_time = attendance.departure_time.strftime('%H:%M') if attendance.departure_time else ''
                arg_overtime = attendance.overtime.strftime('%H:%M') if attendance.overtime else '00:00'
                overtime_str = calculate_hours(arrival_time, departure_time, arg_overtime)
                overtime_hours, overtime_minutes = map(int, overtime_str.split(':'))
                overtime = timedelta(hours=overtime_hours, minutes=overtime_minutes)

            total_overtime += overtime

        total_hours, remainder = divmod(total_overtime.total_seconds(), 3600)
        total_minutes, _ = divmod(remainder, 60)
        formatted_total_overtime = f"{int(total_hours):02}:{int(total_minutes):02}"

    return formatted_total_overtime
