from datetime import date

from aiogram import Router, types

from database.utils.create_attendance import create_attendance
from database.utils.get_attendance import get_attendance
from database.utils.get_employee import get_employee
from database.utils.update_attendance import update_attendance
from keyboards.start_keyboard import start_keyboard
from utils.get_current_time import get_current_time
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
