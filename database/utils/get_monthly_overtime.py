from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session

from database.main import SessionLocal
from database.models.models import Attendance


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
            if attendance.departure_time:
                is_weekend = attendance.date.weekday() >= 5
                if is_weekend:
                    if attendance.arrival_time:
                        overtime = datetime.combine(attendance.date, attendance.departure_time) - datetime.combine(attendance.date, attendance.arrival_time)
                    else:
                        continue
                else:
                    if attendance.departure_time > time(21, 0):
                        overtime = datetime.combine(attendance.date, attendance.departure_time) - datetime.combine(attendance.date, time(21, 0))

                total_overtime += overtime

        total_hours, remainder = divmod(total_overtime.total_seconds(), 3600)
        total_minutes, _ = divmod(remainder, 60)
        formatted_total_overtime = f"{int(total_hours):02}:{int(total_minutes):02}"

    return formatted_total_overtime
