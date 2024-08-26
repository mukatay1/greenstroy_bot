from datetime import date, datetime, time

from aiogram import Router, types

from database.utils.create_attendance import create_attendance
from database.utils.get_attendance import get_attendance
from database.utils.get_employee import get_employee
from database.utils.update_attendance import update_attendance
from keyboards.start_keyboard import start_keyboard
from utils.get_current_time import get_current_time
from utils.get_previous_day import get_previous_day
from utils.is_employee_late import is_employee_late
from utils.is_weekend import is_weekend

router = Router()


@router.message(lambda message: message.text == "Пришел")
async def arrival_handler(message: types.Message):
    user_id = message.from_user.id
    current_date = date.today()

    keyboard = start_keyboard(str(user_id))
    employee = get_employee(str(user_id))

    if employee:
        attendance = get_attendance(
            employee_id=employee.id,
            date=current_date
        )

        if attendance:
            if attendance.check:
                update_attendance(
                    attendance_id=attendance.id,
                    arrival_time=get_current_time(),
                    check=False
                )
                response_message = "Время прибытия успешно отмечено!"
                if is_weekend(current_date):
                    response_message += " Отличная работа, что пришли в выходной день!"
                await message.answer(response_message, reply_markup=keyboard)
            else:
                await message.answer("Вы уже отметили прибытие сегодня.", reply_markup=keyboard)
        else:
            is_late = False
            if not is_weekend(current_date):
                is_late = is_employee_late()

            create_attendance(
                employee_id=employee.id,
                date=current_date,
                arrival_time=get_current_time(),
                late=is_late
            )
            response_message = "Время прибытия успешно отмечено!"
            if is_late and not is_weekend(current_date):
                response_message += " К сожалению, вы опоздали."
            if is_weekend(current_date):
                response_message += " Отличная работа, что пришли в выходной день!"
            await message.answer(response_message, reply_markup=keyboard)
    else:
        await message.answer(
            "Вы не зарегистрированы. Пожалуйста, используйте команду /start для регистрации.",
            reply_markup=keyboard
        )


@router.message(lambda message: message.text == "Ушел")
async def departure_handler(message: types.Message):
    user_id = message.from_user.id
    current_date = date.today()
    keyboard = start_keyboard(str(user_id))
    employee = get_employee(str(user_id))

    if employee:
        attendance = get_attendance(
            employee_id=employee.id,
            date=current_date
        )
        if attendance and attendance.arrival_time:
            update_attendance(
                attendance_id=attendance.id,
                departure_time=get_current_time()
            )
            await message.answer("Время ухода успешно отмечено!", reply_markup=keyboard)
        else:
            await message.answer("Вы не отметили прибытие или уже отметили уход.", reply_markup=keyboard)
    else:
        await message.answer("Вы не зарегистрированы. Пожалуйста, используйте команду /start для регистрации.", reply_markup=keyboard)


@router.message(lambda message: message.text == "Переработка")
async def overtime_handler(message: types.Message):
    user_id = str(message.from_user.id)
    keyboard = start_keyboard(user_id)
    employee = get_employee(user_id)
    current_time = datetime.now().time()
    cutoff_time = time(6, 0)

    if current_time >= cutoff_time:
        await message.answer(
            "Запись переработки доступна только до 6:00 утра. Пожалуйста, попробуйте снова до этого времени.",
            reply_markup=keyboard
        )
        return

    try:
        formatted_time = datetime.now().strftime("%H:%M")
        overtime_time = datetime.strptime(formatted_time, "%H:%M").time()

        previous_day = get_previous_day()
        if employee:
            attendance = get_attendance(
                employee_id=employee.id,
                date=previous_day
            )
            if attendance:
                update_attendance(
                    attendance_id=attendance.id,
                    overtime=overtime_time
                )

                await message.answer(
                    f"Переработка за {previous_day} успешно записана: {overtime_time.strftime('%H:%M')}.",
                    reply_markup=keyboard
                )
            else:
                await message.answer(
                    f"Не удалось найти запись о посещении на {previous_day}. Пожалуйста, проверьте данные.",
                    reply_markup=keyboard
                )
        else:
            await message.answer(
                "Не удалось найти сотрудника. Пожалуйста, попробуйте снова.",
                reply_markup=keyboard
            )

    except ValueError:
        await message.answer(
            "Произошла ошибка при обработке времени. Пожалуйста, попробуйте снова.",
            reply_markup=keyboard
        )