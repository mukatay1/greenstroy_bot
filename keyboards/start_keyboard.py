import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard(user_id: str) -> ReplyKeyboardMarkup:
    ADMIN_ID = os.getenv('ADMIN_ID')
    SUPER_ADMIN = os.getenv('SUPERADMIN')
    is_admin = user_id in ADMIN_ID

    if user_id in SUPER_ADMIN:
        kb = [
            [KeyboardButton(text="Пришел"), KeyboardButton(text="Ушел"), KeyboardButton(text="Переработка")],
            [KeyboardButton(text="Отъезд"), KeyboardButton(text="За ранее отпросился"), KeyboardButton(text="Отчет")],
            [KeyboardButton(text="Табель"), KeyboardButton(text="Опоздавшие"), KeyboardButton(text="Выбрать город")],
        ]
    else:
        if is_admin:
            kb = [
                [KeyboardButton(text="Пришел"), KeyboardButton(text="Ушел"), KeyboardButton(text="Переработка")],
                [KeyboardButton(text="Отъезд"), KeyboardButton(text="За ранее отпросился"), KeyboardButton(text="Отчет")],
                [KeyboardButton(text="Табель"), KeyboardButton(text="Опоздавшие")],
            ]
        else:
            kb = [
                [KeyboardButton(text="Пришел"), KeyboardButton(text="Ушел"), KeyboardButton(text="Переработка")],
                [KeyboardButton(text="Отъезд"), KeyboardButton(text="За ранее отпросился")]
            ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку",
        one_time_keyboard=False
    )
    return keyboard