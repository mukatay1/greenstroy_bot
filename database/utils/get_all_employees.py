import os

from sqlalchemy import not_

from database.main import SessionLocal
from database.models.City import City
from database.models.models import Employee
from utils.string_to_list import string_to_list


def get_all_employees(city: City) -> list[Employee]:
    IGNORE_WORKERS = string_to_list(os.getenv("IGNORE_WORKERS"))
    with SessionLocal() as db:
        employees = db.query(Employee).filter(
            not_(Employee.telegram_id.in_(IGNORE_WORKERS)),
            Employee.city == city
        ).all()
    return employees


def get_all_employees_without_ignored(city: City) -> list[Employee]:
    with SessionLocal() as db:
        employees = db.query(Employee).filter(
            Employee.city == city
        ).all()
    return employees
