from datetime import date

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from config import supervisors
from database.utils.create_attendance import create_attendance
from database.utils.get_attendance import get_attendance
from database.utils.get_employee import get_employee
from database.utils.update_attendance import update_attendance
from keyboards.departure_type_keyboard import departure_type_keyboard
from keyboards.return_keyboard import return_keyboard
from keyboards.supervisor_keyboard import supervisor_keyboard
from utils.get_current_time import get_current_time

router = Router()


class Form(StatesGroup):
    choosing_departure_type = State()
    choosing_supervisor = State()
    waiting_for_reason = State()
    waiting_for_departure_time = State()


@router.message(lambda message: message.text == "Отъезд")
async def departure_command_handler(message: types.Message, state: FSMContext):
    current_departure_time = get_current_time()
    await state.update_data(departure_time_actual=current_departure_time)

    await message.answer("Выберите тип отъезда:", reply_markup=departure_type_keyboard())
    await state.set_state(Form.choosing_departure_type)


@router.callback_query(lambda c: c.data.startswith('type_'))
async def handle_departure_type(callback_query: CallbackQuery, state: FSMContext):
    departure_type = callback_query.data.split('_')[1].capitalize()
    departure_type_mapping = {
        "Object": "Объект",
        "Personal": "Личный"
    }

    if departure_type not in departure_type_mapping:
        await callback_query.message.answer("Пожалуйста, выберите 'Объект' или 'Личный'.")
        return

    departure_type_russian = departure_type_mapping[departure_type]
    await state.update_data(departure_type=departure_type_russian)
    await callback_query.message.answer("Выберите, у кого отпрашиваетесь:", reply_markup=supervisor_keyboard())
    await state.set_state(Form.choosing_supervisor)
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith('supervisor_'))
async def handle_supervisor(callback_query: CallbackQuery, state: FSMContext):
    try:
        supervisor_index = int(callback_query.data.split('_', 1)[1])

        if supervisor_index >= len(supervisors):
            await callback_query.message.answer("Пожалуйста, выберите одного из руководителей.")
            return

        supervisor = supervisors[supervisor_index]
        await state.update_data(supervisor=supervisor)
        await callback_query.message.answer("Пожалуйста, напишите причину вашего отсутствия.")
        await state.set_state(Form.waiting_for_reason)
        await callback_query.answer()
    except Exception as e:
        print(f"Error in handle_supervisor: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке вашего выбора.")


@router.message(Form.waiting_for_reason)
async def handle_absence_reason(message: types.Message, state: FSMContext):
    reason = message.text
    data = await state.get_data()
    departure_type = data.get("departure_type")
    supervisor = data.get("supervisor")
    departure_time_actual = data.get("departure_time_actual")
    await state.update_data(departure_reason=reason)

    response_text = (
        f"<b>📩 Отчёт об отъезде</b>\n\n"
        f"<b>Тип отъезда:</b> <i>{departure_type}</i>\n"
        f"<b>Время отъезда:</b> <i>{departure_time_actual}</i>\n"
        f"<b>Руководитель:</b> <i>{supervisor}</i>\n"
        f"<b>Причина:</b>\n"
        f"{reason}"
        )
    keyboard = return_keyboard()
    await message.answer(response_text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'return')
async def return_data(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    current_date = date.today()
    employee = get_employee(str(user_id))
    existing_attendance = get_attendance(
        employee_id=employee.id,
        date=current_date
    )
    data = await state.get_data()
    departure_type = data.get("departure_type")
    departure_reason = data.get("departure_reason")
    supervisor = data.get("supervisor")
    departure_time_actual = data.get("departure_time_actual").replace(microsecond=0)
    return_time = get_current_time()

    if existing_attendance:
        update_attendance(
            attendance_id=existing_attendance.id,
            departure_type=departure_type,
            departure_reason=departure_reason,
            supervisor=supervisor,
            departure_time_actual=departure_time_actual,
            return_time=return_time

        )

        await callback_query.message.answer("Ваше возвращение зафиксировано. Спасибо!")
    else:
        create_attendance(
            employee_id=employee.id,
            departure_type=departure_type,
            departure_reason=departure_reason,
            supervisor=supervisor,
            departure_time_actual=departure_time_actual,
            return_time=return_time,
            check=True,
            date=current_date

        )

        await callback_query.message.answer("Ваше возвращение зафиксировано. Спасибо!")

    await state.clear()
