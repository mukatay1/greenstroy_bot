from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def date_keyboard() -> InlineKeyboardMarkup:
    kb = []
    today = datetime.today()

    for i in range(7):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        button = InlineKeyboardButton(text=date_str, callback_data=f"report_{date_str}")
        kb.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard