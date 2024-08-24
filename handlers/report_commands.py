from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, CallbackQuery

from config import months_russian
from database.main import SessionLocal
from database.models.models import Attendance
from database.utils.get_all_attendances import get_all_attendances
from database.utils.get_all_employees import get_all_employees
from database.utils.get_employee_city import get_employee_city
from keyboards.date_keyboard import date_keyboard
from utils.excel_report import excel_report
from utils.get_first_day_of_month import get_first_day_of_month
from utils.get_last_day_of_month import get_last_day_of_month
from utils.late_excel_report import late_excel_report
from utils.has_admin_privileges import check_admin_privileges
from utils.parse_report_date import parse_report_date
from utils.str_to_date import str_to_date

router = Router()


@router.message(lambda message: message.text == "Опоздавшие")
async def late_report_handler(message: types.Message):
    user_id = message.from_user.id
    city = get_employee_city(str(user_id))
    error_message = check_admin_privileges(str(user_id))

    if error_message:
        await message.answer(error_message)
        return

    db = SessionLocal()

    now = datetime.now()
    first_day_of_month = get_first_day_of_month()
    last_day_of_month = get_last_day_of_month()
    name_of_month_on_rus = months_russian[now.month]

    employees = get_all_employees(city)

    data = []
    for employee in employees:

        late_attendances = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.late is True,
            Attendance.date >= first_day_of_month,
            Attendance.date <= last_day_of_month
        ).all()

        late_days = [attendance.date for attendance in late_attendances]
        late_days_str = ', '.join([str(day) for day in late_days])

        data.append({
            "ФИО": employee.fio,
            "Телеграмм - ID": employee.telegram_id,
            "Телеграмм Ник": employee.full_name,
            "Количество опозданий": len(late_attendances),
            "Дни опозданий": late_days_str
        })

    report_file = late_excel_report(data, name_of_month_on_rus, city)

    report_document = FSInputFile(report_file)
    await message.answer_document(
        report_document,
        caption=f"Отчет по опозданиям сотрудников за {name_of_month_on_rus} - г.{city.value}"
    )

    db.close()


async def send_report(message: types.Message, selected_date: str, user_id: int) -> None:
    date = str_to_date(selected_date)
    city = get_employee_city(str(user_id))
    employees = get_all_employees(city)
    attendances = get_all_attendances(date=date)
    data = []

    for employee in employees:
        employee_attendance = None
        for attendance in attendances:
            if attendance.employee_id == employee.id:
                employee_attendance = attendance
                break

        if employee_attendance:
            data.append({
                "ФИО": employee.fio,
                "Дата": date,
                "Телеграмм - ID": employee.telegram_id,
                "Телеграмм Ник": employee.full_name,
                "Время прибытия": employee_attendance.arrival_time,
                "Время ухода": employee_attendance.departure_time,
                "Тип отъезда": employee_attendance.departure_type,
                "Руководитель": employee_attendance.supervisor,
                "Причина": employee_attendance.departure_reason,
                "Время отъезда": employee_attendance.departure_time_actual,
                "Время возвращения": employee_attendance.return_time,
                "За ранее отпросился": employee_attendance.skip_status
            })
        else:
            data.append({
                "ФИО": employee.fio,
                "Дата": date,
                "Телеграмм - ID": employee.telegram_id,
                "Телеграмм Ник": employee.full_name,
                "Время прибытия": '',
                "Время ухода": '',
                "Тип отъезда": '',
                "Руководитель": '',
                "Причина": '',
                "Время отъезда": '',
                "Время возвращения": '',
                "За ранее отпросился": ''
            })

    report_file = excel_report(data, f"{selected_date}", city)

    report_document = FSInputFile(report_file)
    await message.answer_document(report_document, caption=f"Отчет сотрудников за {selected_date} - г.{city.value}")


@router.callback_query(lambda c: c.data and c.data.startswith("report_"))
async def process_date_callback(callback_query: CallbackQuery):
    selected_date = callback_query.data.split("_")[1]
    await send_report(callback_query.message, selected_date, callback_query.from_user.id)
    await callback_query.answer()


@router.message(lambda message: message.text == "Отчет")
async def report_button_handler(message: types.Message):
    user_id = message.from_user.id
    error_message = check_admin_privileges(str(user_id))

    if error_message:
        await message.answer(error_message)
        return

    keyboard = date_keyboard()
    await message.answer(
            "Чтобы получить отчет за конкретный день, напишите команду в формате: /report YYYY-MM-DD, где YYYY-MM-DD — это дата в формате год-месяц-день. Например: /report 2024-07-20.")
    await message.answer("Выберите дату для отчета:", reply_markup=keyboard)


@router.message(Command(commands=['report']))
async def report_handler(message: types.Message):
    user_id = message.from_user.id
    city = get_employee_city(str(user_id))

    try:
        report_date = parse_report_date(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    employees = get_all_employees(city)
    attendances = get_all_attendances(date=report_date)

    data = []

    for employee in employees:
        employee_attendance = None
        for attendance in attendances:
            if attendance.employee_id == employee.id:
                employee_attendance = attendance
                break

        if employee_attendance:
            data.append({
                "ФИО": employee.fio,
                "Дата": report_date,
                "Телеграмм - ID": employee.telegram_id,
                "Телеграмм Ник": employee.full_name,
                "Время прибытия": employee_attendance.arrival_time,
                "Время ухода": employee_attendance.departure_time,
                "Тип отъезда": employee_attendance.departure_type,
                "Руководитель": employee_attendance.supervisor,
                "Причина": employee_attendance.departure_reason,
                "Время отъезда": employee_attendance.departure_time_actual,
                "Время возвращения": employee_attendance.return_time,
                "За ранее отпросился": employee_attendance.skip_status

            })
        else:
            data.append({
                "ФИО": employee.fio,
                "Дата": report_date,
                "Телеграмм - ID": employee.telegram_id,
                "Телеграмм Ник": employee.full_name,
                "Время прибытия": '',
                "Время ухода": '',
                "Тип отъезда": '',
                "Руководитель": '',
                "Причина": '',
                "Время отъезда": '',
                "Время возвращения": '',
                "За ранее отпросился": ''
            })

    report_file = excel_report(data, f"{report_date}", city)

    report_document = FSInputFile(report_file)
    await message.answer_document(report_document, caption=f"Отчет сотрудников за {report_date} - г.{city.value}")


