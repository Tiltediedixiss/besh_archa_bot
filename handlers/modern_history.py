from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.texts import MODERN_HISTORY, TODAY_PLAN, ARCHIE_FINAL_MESSAGE, VIDEO_LEGEND_OFFER, DAY_1_COMPLETE
from data.files import MODERN_HISTORY_PHOTOS, GOOD_JOB_STICKER_ID
from keyboards.main_menu import modern_history_keyboard, main_menu_keyboard, today_plan_keyboard, video_legend_keyboard, day_completion_keyboard
from data.progress import progress_manager

def register_modern_history(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "modern_history")
    async def modern_history(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        await start_modern_history_module(callback_query.message, user_id)

    @dp.callback_query_handler(lambda c: c.data == "video_legend_russian")
    async def video_legend_russian(callback_query: types.CallbackQuery):
        await callback_query.message.answer("🎬 Фильм о Миссии, Видении и Ценностях Компании на русском языке:\nhttps://youtu.be/z-zLfkeyx70")
        # After showing video, end Day 1
        await end_day_1(callback_query.message)

    @dp.callback_query_handler(lambda c: c.data == "video_legend_kyrgyz")
    async def video_legend_kyrgyz(callback_query: types.CallbackQuery):
        await callback_query.message.answer("🎬 Фильм о Миссии, Видении и Ценностях Компании на кыргызском языке:\nhttps://youtu.be/Z0gGhzk5AJg")
        # After showing video, end Day 1
        await end_day_1(callback_query.message)

    @dp.callback_query_handler(lambda c: c.data == "skip_videos")
    async def skip_videos(callback_query: types.CallbackQuery):
        # After skipping videos, end Day 1
        await end_day_1(callback_query.message)

    async def end_day_1(message: types.Message):
        """End Day 1 with final message and sticker only (без дублирующих блоков)"""
        try:
            await message.answer_sticker(GOOD_JOB_STICKER_ID)
        except:
            pass
        await message.answer(ARCHIE_FINAL_MESSAGE)

    @dp.callback_query_handler(lambda c: c.data == "today_plan")
    async def today_plan(callback_query: types.CallbackQuery):
        await callback_query.message.answer(TODAY_PLAN, reply_markup=today_plan_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "video_legend_offer")
    async def video_legend_offer(callback_query: types.CallbackQuery):
        """Показывает предложение посмотреть видео о легенде"""
        user_id = callback_query.from_user.id
        await callback_query.message.answer(VIDEO_LEGEND_OFFER, reply_markup=video_legend_keyboard(user_id))

    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def main_menu(callback_query: types.CallbackQuery):
        await callback_query.message.answer("Главное меню:", reply_markup=main_menu_keyboard(callback_query.from_user.id))

async def start_modern_history_module(message: types.Message, user_id: int):
    """Запускает модуль современной истории с кнопкой 'Дальше'"""
    # Отмечаем модуль как завершенный
    progress_manager.update_module_progress(user_id, "Современная история", 1)

    if MODERN_HISTORY_PHOTOS[0]:
        try:
            await message.answer_photo(MODERN_HISTORY_PHOTOS[0], caption=MODERN_HISTORY, reply_markup=modern_history_keyboard())
        except:
            await message.answer(MODERN_HISTORY, reply_markup=modern_history_keyboard())
    else:
        await message.answer(MODERN_HISTORY, reply_markup=modern_history_keyboard()) 