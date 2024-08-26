import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from config import DEBUG
from database.main import init_db

from handlers.base_commands import router as base_router
from handlers.attendance_commands import router as attendance_router
from handlers.report_commands import router as report_router
from handlers.departure_commands import router as departure_router
from handlers.chat_commands import router as chat_router
from handlers.absent_commands import router as absent_router
from handlers.reportcard_commands import router as card_router
from utils.schedule import schedule_jobs

load_dotenv()

if DEBUG:
    API_TOKEN = os.getenv('TEST_BOT_TOKEN')
else:
    API_TOKEN = os.getenv('BOT_TOKEN')

storage = MemoryStorage()


async def main() -> None:
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(base_router)
    dp.include_router(attendance_router)
    dp.include_router(report_router)
    dp.include_router(departure_router)
    dp.include_router(absent_router)
    dp.include_router(card_router)
    dp.include_router(chat_router)

    init_db()
    schedule_jobs(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())