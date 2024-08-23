from datetime import datetime, time


def is_employee_late() -> bool:
    late_time = time(9, 5)
    current_time = datetime.now().time()
    return current_time > late_time

