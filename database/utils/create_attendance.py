from datetime import date, time

from database.main import SessionLocal
from database.models.models import Attendance


def create_attendance(
        employee_id: int,
        date: date,
        arrival_time: time = None,
        departure_time: time = None,
        late: bool = False,
        departure_type: str = None,
        departure_reason: str = None,
        supervisor: str = None,
        departure_time_actual: time = None,
        return_time: time = None,
        check: bool = False,
        skip_status: str = None
) -> Attendance:
    with SessionLocal() as db:
        attendance = Attendance(
            employee_id=employee_id,
            date=date,
            arrival_time=arrival_time,
            departure_time=departure_time,
            late=late,
            departure_type=departure_type,
            departure_reason=departure_reason,
            supervisor=supervisor,
            departure_time_actual=departure_time_actual,
            return_time=return_time,
            check=check,
            skip_status=skip_status
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance