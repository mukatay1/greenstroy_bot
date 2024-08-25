from aiogram import Router, html
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.models.City import City
from database.utils.create_employee import create_employee
from database.utils.get_employee import get_employee
from database.utils.update_employee import update_employee
from keyboards.city_keyboards import city_keyboard
from keyboards.start_keyboard import start_keyboard

router = Router()


class Form(StatesGroup):
    city = State()
    waiting_for_full_name = State()


@router.message(Command(commands=["start", "help"]))
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    keyboard = start_keyboard(str(user_id))
    employee = get_employee(str(user_id))

    if not employee:
        welcome_text = (
            f"Здравствуйте, {html.bold(message.from_user.full_name)}! Добро пожаловать в систему учета времени."
        )
        await message.answer(welcome_text)

        await message.answer("Пожалуйста, выберите ваш город:", reply_markup=city_keyboard('start'))
        await state.set_state(Form.city)
    else:
        await message.answer(
            f"Здравствуйте, {html.bold(full_name)}! Вы уже зарегистрированы.",
            reply_markup=keyboard
        )


@router.callback_query(lambda c: c.data.startswith('start_'))
async def handle_city_selection(callback_query: types.CallbackQuery, state: FSMContext):
    city_str = callback_query.data.split('_')[1]
    city = City[city_str]

    await state.update_data(city=city)
    await callback_query.message.answer("Пожалуйста, укажите ваше ФИО.")
    await state.set_state(Form.waiting_for_full_name)


@router.message(Form.waiting_for_full_name)
async def handle_full_name(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    keyboard = start_keyboard(str(user_id))

    state_data = await state.get_data()
    city = state_data.get('city')

    existing_employee = get_employee(str(user_id))

    if existing_employee:
        update_employee(
            user_id=str(user_id),
            fio=message.text
        )
    else:
        create_employee(
            telegram_id=str(user_id),
            full_name=full_name,
            fio=message.text,
            city=city
        )

    await message.answer(
        f"Здравствуйте, {html.bold(full_name)}! Вы успешно зарегистрированы.",
        reply_markup=keyboard
    )
    await state.clear()


@router.message(lambda message: message.text == "Выбрать город")
async def city_command_handler(message: types.Message):
    keyboard = city_keyboard('change')
    await message.answer('Пожалуйста, выберите город из списка ниже.', reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('change_'))
async def handle_city_change(callback_query: types.CallbackQuery):
    user_id = str(callback_query.from_user.id)
    city_str = callback_query.data.split('_')[1]
    city = City[city_str]

    keyboard = start_keyboard(user_id)
    employee = get_employee(user_id)
    if employee:
        update_employee(
            user_id=user_id,
            city=city
        )
        message = f'Город успешно изменен на {city.value}. Все дальнейшие действия будут связаны с этим городом.'
        await callback_query.message.answer(message, reply_markup=keyboard)
    else:
        message = "К сожалению, не удалось найти сотрудника. Пожалуйста, проверьте введенные данные и попробуйте снова."
        await callback_query.message.answer(message, reply_markup=keyboard)
