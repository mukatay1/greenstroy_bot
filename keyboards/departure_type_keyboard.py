from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def departure_type_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Объект", callback_data="type_object")],
        [InlineKeyboardButton(text="Личный", callback_data="type_personal")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard