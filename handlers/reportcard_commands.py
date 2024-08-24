from datetime import timedelta

from aiogram import Router, types
from aiogram.types import FSInputFile

from database.utils.get_all_employees import get_all_employees
from database.utils.get_attendance import get_attendance
from database.utils.get_employee_city import get_employee_city
from database.utils.get_monthly_overtime import get_monthly_overtime
from keyboards.start_keyboard import start_keyboard
from utils.calculate_hours import calculate_hours
from utils.excel_card_report import excel_card_report
from utils.get_first_day_of_month import get_first_day_of_month
from utils.get_last_day_of_month import get_last_day_of_month
from utils.get_today_month_name import get_today_month_name
from utils.get_weekday import get_weekday
from utils.has_admin_privileges import check_admin_privileges

router = Router()


@router.message(lambda message: message.text == "Табель")
async def month_report_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    city = get_employee_city(str(user_id))
    error_message = check_admin_privileges(str(user_id))

    if error_message:
        await message.answer(error_message)
        return

    rus_month = get_today_month_name()
    first_day = get_first_day_of_month()
    last_day = get_last_day_of_month()
    employees = get_all_employees(city=city)

    dates = [first_day + timedelta(days=x) for x in range((last_day - first_day).days + 1)]
    columns = (
            ['№', 'ФИО', 'Время'] +
            [date.strftime('%Y-%m-%d') + ' (' + get_weekday(date) + ')' for date in dates] +
            ['Переработка (ч)']
    )
    data = []

    for index, employee in enumerate(employees, start=1):
        row_arrival = [index, employee.fio, 'Время прихода']
        row_departure = ['', '', 'Время ухода']
        row_third = ['', '', 'Кол-во часов']
        for single_date in dates:
            attendance = get_attendance(
                employee_id=employee.id,
                date=single_date.date()
            )
            if attendance:
                arrival_time = attendance.arrival_time.strftime('%H:%M') if attendance.arrival_time else ''
                departure_time = attendance.departure_time.strftime('%H:%M') if attendance.departure_time else ''
                worked_hours = calculate_hours(arrival_time, departure_time)

                row_arrival.append(arrival_time)
                row_departure.append(departure_time)
                row_third.append(worked_hours)
            else:
                row_arrival.append("")
                row_departure.append("")
                row_third.append("00:00")

        row_arrival.append("")
        row_departure.append("")
        row_third.append(get_monthly_overtime(employee_id=employee.id))

        data.append(row_arrival)
        data.append(row_departure)
        data.append(row_third)

    file_path = excel_card_report(data, columns, rus_month, city)

    keyboard = start_keyboard(str(user_id))

    report_document = FSInputFile(file_path)
    await message.answer_document(
        report_document,
        caption=f'Табель за {rus_month} - г.{city.value}',
        reply_markup=keyboard
    )