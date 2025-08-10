from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.texts import LEGEND_STEPS
from data.files import LEGEND_PHOTOS, LEGEND_STICKER_ID
from keyboards.main_menu import legend_keyboard, legend_next_keyboard, modern_history_keyboard, main_menu_keyboard
from data.progress import progress_manager

def register_legend(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "legend_start")
    async def legend_entry(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        await start_legend_module(callback_query.from_user.id, callback_query.message)

    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def legend_to_main_menu(callback_query: types.CallbackQuery):
        await callback_query.message.answer("Вы в главном меню! (Здесь будет следующий этап или меню)", reply_markup=main_menu_keyboard())

    @dp.callback_query_handler(lambda c: c.data.startswith("legend_next_"))
    async def legend_next(callback_query: types.CallbackQuery):
        step = int(callback_query.data.split("_")[-1])
        user_id = callback_query.from_user.id
        await show_legend_step(callback_query.message, step, user_id)

async def start_legend_module(user_id: int, message: types.Message):
    """Запускает модуль легенды с первым шагом"""
    # Отмечаем модуль как начатый
    progress_manager.update_module_progress(user_id, "Легенда компании", 1)
    
    # Сначала отправляем стикер для легенды
    try:
        await message.answer_sticker(LEGEND_STICKER_ID)
    except:
        await message.answer("📖 Начинаем легенду!")
    
    # Показываем первый шаг
    await show_legend_step(message, 0, user_id)

async def show_legend_step(message: types.Message, step: int, user_id: int):
    """Показывает конкретный шаг легенды"""
    if step >= len(LEGEND_STEPS):
        return
    
    text = LEGEND_STEPS[step]
    photo = LEGEND_PHOTOS[step] if step < len(LEGEND_PHOTOS) else None
    
    # Если это предпоследний шаг (последний смысловой), после него отправляем коннектор
    if step == len(LEGEND_STEPS) - 2:
        if photo:
            try:
                await message.answer_photo(photo, caption=text)
            except:
                await message.answer(text)
        else:
            await message.answer(text)
        
        connector_text = LEGEND_STEPS[-1]
        from keyboards.main_menu import legend_to_modern_history_keyboard
        await message.answer(connector_text, reply_markup=legend_to_modern_history_keyboard())
        return
    
    # Если это финальный шаг-коннектор, ничего не делаем (он отправляется выше)
    if step == len(LEGEND_STEPS) - 1:
        return
    
    # Обычные шаги
    if photo:
        try:
            await message.answer_photo(photo, caption=text, reply_markup=legend_next_keyboard(step, len(LEGEND_STEPS)))
        except:
            await message.answer(text, reply_markup=legend_next_keyboard(step, len(LEGEND_STEPS)))
    else:
        await message.answer(text, reply_markup=legend_next_keyboard(step, len(LEGEND_STEPS))) 