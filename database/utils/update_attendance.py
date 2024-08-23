from datetime import time

from database.main import SessionLocal
from database.models.models import Attendance


def update_attendance(
        attendance_id: int,
        arrival_time: time = None,
        departure_time: time = None,
        late: bool = None,
        departure_type: str = None,
        departure_reason: str = None,
        supervisor: str = None,
        departure_time_actual: time = None,
        return_time: time = None,
        check: bool = None,
        skip_time: time = None
) -> Attendance:
    with SessionLocal() as db:
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()

        if attendance:
            if arrival_time is not None:
                attendance.arrival_time = arrival_time
            if departure_time is not None:
                attendance.departure_time = departure_time
            if late is not None:
                attendance.late = late
            if departure_type is not None:
                attendance.departure_type = departure_type
            if departure_reason is not None:
                attendance.departure_reason = departure_reason
            if supervisor is not None:
                attendance.supervisor = supervisor
            if departure_time_actual is not None:
                attendance.departure_time_actual = departure_time_actual
            if return_time is not None:
                attendance.return_time = return_time
            if check is not None:
                attendance.check = check
            if skip_time is not None:
                attendance.skip_time = skip_time

            db.commit()
            db.refresh(attendance)

        return attendance
