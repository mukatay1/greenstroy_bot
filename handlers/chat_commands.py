from aiogram import Router, Bot, types

from config import DEBUG
from database.utils.get_all_employees import get_all_employees_without_ignored
from database.utils.get_employee import get_employee
from database.utils.get_employee_city import get_employee_city

router = Router()


async def universal_message_handler(message: types.Message, bot: Bot) -> None:
    user_id = message.from_user.id
    employee = get_employee(str(user_id))
    employee_name = employee.fio if employee and employee.fio else message.from_user.full_name
    message_text = (
        f"<b>📩 Новое сообщение</b>\n\n"
        f"<b>От:</b> <i>{employee_name}</i>\n"
        f"<b>Сообщение:</b>\n"
        f"{message.text}"
    )
    await send_message_to_all_employees(bot, message_text, message.from_user.id)


async def send_message_to_all_employees(bot: Bot, message_text: str, user_id: int) -> None:
    city = get_employee_city(str(user_id))
    employees = get_all_employees_without_ignored(city)
    for employee in employees:
        try:
            if DEBUG:
                print(message_text)
            else:
                await bot.send_message(employee.telegram_id, message_text)
        except Exception as e:
            print(f"Не удалось отправить сообщение сотруднику {employee.telegram_id}: {e}")


@router.message()
async def handle_all_messages(message: types.Message, bot: Bot) -> None:
    await universal_message_handler(message, bot)


