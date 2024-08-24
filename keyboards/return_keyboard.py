from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def return_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Приезд", callback_data="return")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard