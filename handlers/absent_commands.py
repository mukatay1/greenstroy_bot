from datetime import date

from aiogram import Router, types

from database.utils.create_attendance import create_attendance
from database.utils.get_attendance import get_attendance
from database.utils.get_employee import get_employee
from database.utils.update_attendance import update_attendance
from keyboards.start_keyboard import start_keyboard

router = Router()


@router.message(lambda message: message.text == "За ранее отпросился")
async def skip_command_handler(message: types.Message):
    user_id = message.from_user.id

    employee = get_employee(str(user_id))
    attendance = get_attendance(
        employee_id=employee.id,
        date=date.today()
    )

    keyboard = start_keyboard(str(user_id))

    if attendance:
        update_attendance(
            attendance_id=attendance.id,
            skip_status='За ранее отпросился'
        )
        await message.answer("Вы успешно отпросились. ", reply_markup=keyboard)
    else:
        create_attendance(
            employee_id=employee.id,
            date=date.today(),
            skip_status='За ранее отпросился',
            check=True
        )
        await message.answer("Вы успешно отпросились! ", reply_markup=keyboard)

