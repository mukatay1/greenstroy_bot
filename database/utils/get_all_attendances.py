from datetime import date, time

from database.main import SessionLocal
from database.models.models import Attendance


def get_all_attendances(
        employee_id: int = None,
        date: date = None,
        arrival_time: time = None,
        departure_time: time = None,
        late: bool = None,
        departure_type: str = None,
        departure_reason: str = None,
        supervisor: str = None,
        departure_time_actual: time = None,
        return_time: time = None,
        check: bool = None,
        skip_status: str = None
) -> list[Attendance]:
    with SessionLocal() as db:
        query = db.query(Attendance)

        if employee_id is not None:
            query = query.filter(Attendance.employee_id == employee_id)
        if date is not None:
            query = query.filter(Attendance.date == date)
        if arrival_time is not None:
            query = query.filter(Attendance.arrival_time == arrival_time)
        if departure_time is not None:
            query = query.filter(Attendance.departure_time == departure_time)
        if late is not None:
            query = query.filter(Attendance.late == late)
        if departure_type is not None:
            query = query.filter(Attendance.departure_type == departure_type)
        if departure_reason is not None:
            query = query.filter(Attendance.departure_reason == departure_reason)
        if supervisor is not None:
            query = query.filter(Attendance.supervisor == supervisor)
        if departure_time_actual is not None:
            query = query.filter(Attendance.departure_time_actual == departure_time_actual)
        if return_time is not None:
            query = query.filter(Attendance.return_time == return_time)
        if check is not None:
            query = query.filter(Attendance.check == check)
        if skip_status is not None:
            query = query.filter(Attendance.skip_status == skip_status)

        return query.all()
