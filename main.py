import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers.start import register_start
from handlers.legend import register_legend
from handlers.modern_history import register_modern_history
from handlers.ceo_greeting import register_ceo_greeting
from handlers.get_file_id import register_get_file_id
from handlers.mission import register_mission
from handlers.news import register_news
from handlers.main_menu import register_main_menu
from handlers.company_info import register_company_info
from handlers.important_docs import register_important_docs
from handlers.progress_handler import register_progress
from handlers.excel_export import register_excel_export

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dp):
    # Отключаем webhook и сбрасываем зависшие обновления, чтобы polling не конфликтовал
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception:
        pass

register_start(dp)
register_legend(dp)
register_modern_history(dp)
register_ceo_greeting(dp)
register_get_file_id(dp)
register_mission(dp)
register_news(dp)
register_main_menu(dp)
register_company_info(dp)
register_important_docs(dp)
register_progress(dp)
register_excel_export(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)