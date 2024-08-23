from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.models.City import City


def city_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text=city.value, callback_data=city.name)] for city in City]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard