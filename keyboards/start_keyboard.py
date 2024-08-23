import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard(user_id: str) -> ReplyKeyboardMarkup:
    ADMIN_ID = os.getenv('ADMIN_ID')
    is_admin = user_id in ADMIN_ID

    if is_admin:
        kb = [
            [KeyboardButton(text="Пришел"), KeyboardButton(text="Ушел")],
            [KeyboardButton(text="Отъезд"), KeyboardButton(text="Отпроситься"), KeyboardButton(text="Отчет")],
            [KeyboardButton(text="Табель"), KeyboardButton(text="Опоздавшие")],
        ]
    else:
        kb = [
            [KeyboardButton(text="Пришел"), KeyboardButton(text="Ушел")],
            [KeyboardButton(text="Отъезд"), KeyboardButton(text="Отпроситься")]
        ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку",
        one_time_keyboard=False
    )
    return keyboard