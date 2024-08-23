from database.main import SessionLocal
from database.models.City import City
from database.models.models import Employee


def create_employee(telegram_id: int, full_name: str, fio: str, city: City) -> Employee:
    with SessionLocal() as db:

        new_employee = Employee(
            telegram_id=telegram_id,
            full_name=full_name,
            fio=fio,
            city=city
        )
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return new_employee
