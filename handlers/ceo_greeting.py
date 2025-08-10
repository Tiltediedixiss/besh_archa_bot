from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.texts import CEO_GREETING
from data.files import CEO_PHOTO_PATH
from keyboards.main_menu import ceo_greeting_keyboard, legend_keyboard
from data.progress import progress_manager
import os

def register_ceo_greeting(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "ceo_greeting")
    async def ceo_greeting(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        await start_ceo_greeting(callback_query.message, user_id)

async def start_ceo_greeting(message: types.Message, user_id: int):
    """Запускает приветствие от CEO с кнопкой 'Дальше'"""
    # Отмечаем модуль как завершенный
    progress_manager.update_module_progress(user_id, "Приветствие от CEO", 1)
    
    # Показываем приветствие от CEO
    if CEO_PHOTO_PATH and os.path.exists(CEO_PHOTO_PATH):
        with open(CEO_PHOTO_PATH, 'rb') as photo:
            await message.answer_photo(photo, caption=CEO_GREETING, parse_mode="Markdown", reply_markup=ceo_greeting_keyboard())
    else:
        await message.answer(CEO_GREETING, parse_mode="Markdown", reply_markup=ceo_greeting_keyboard()) 