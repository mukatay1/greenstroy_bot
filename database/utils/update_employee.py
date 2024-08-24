from typing import Optional

from database.main import SessionLocal
from database.models.City import City
from database.models.models import Employee


def update_employee(
        user_id: str,
        full_name: Optional[str] = None,
        fio: Optional[str] = None,
        city: Optional[City] = None
) -> Employee:
    with SessionLocal() as db:
        employee = db.query(Employee).filter(Employee.telegram_id == user_id).first()

        if not employee:
            raise ValueError(f"Employee with ID {user_id} not found.")

        if full_name is not None:
            employee.full_name = full_name
        if fio is not None:
            employee.fio = fio
        if city is not None:
            employee.city = city

        db.commit()
        db.refresh(employee)

        return employee
