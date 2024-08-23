from database.main import SessionLocal
from database.models.City import City
from database.models.models import Employee


def get_employee_by_city(user_id: int, city: City) -> Employee | None:
    with SessionLocal() as db:
        employee = db.query(Employee).filter(
            Employee.telegram_id == user_id,
            Employee.city == city.value
        ).first()
    return employee
