from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import supervisors


def supervisor_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text=supervisor, callback_data=f"supervisor_{i}")] for i, supervisor in enumerate(supervisors)]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard