from database.models.City import City
from database.utils.get_employee import get_employee


def get_employee_city(user_id: int) -> City:
    employee = get_employee(user_id)
    if employee:
        return employee.city
    else:
        pass
