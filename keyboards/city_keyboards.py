from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.models.City import City


def city_keyboard(action: str) -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text=city.value, callback_data=f'{action}_{city.name}')] for city in City]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard