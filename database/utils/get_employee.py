from database.main import SessionLocal
from database.models.models import Employee


def get_employee(user_id: str) -> Employee:
    with SessionLocal() as db:
        employee = db.query(Employee).filter(Employee.telegram_id == user_id).first()
    return employee
