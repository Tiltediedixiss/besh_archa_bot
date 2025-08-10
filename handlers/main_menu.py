from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.main_menu import main_menu_keyboard, smart_day_menu_keyboard
from data.progress import progress_manager
from keyboards.mission_keyboard import day2_intro_keyboard
from data.files import GOOD_JOB_STICKER_ID
from data.progress import progress_manager

def register_main_menu(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "main_menu")
    async def main_menu(callback_query: types.CallbackQuery):
        """Показывает главное меню с учетом прогресса пользователя"""
        user_id = callback_query.from_user.id
        await callback_query.message.edit_reply_markup(main_menu_keyboard(user_id))
    
    @dp.callback_query_handler(lambda c: c.data == "show_progress")
    async def show_progress(callback_query: types.CallbackQuery):
        """Показывает прогресс пользователя"""
        user_id = callback_query.from_user.id
        progress = progress_manager.get_user_progress(user_id)
        
        summary = progress_manager.get_progress_summary(user_id)
        await callback_query.message.answer(summary, parse_mode='Markdown')
    
    # Больше не перехватываем *_completed, так как кнопки ведут на _start повторно
    
    @dp.callback_query_handler(lambda c: c.data.endswith("_locked"))
    async def show_locked_day(callback_query: types.CallbackQuery):
        """Показывает информацию о заблокированном дне"""
        day = int(callback_query.data.split("_")[1])
        await callback_query.message.answer(f"🔒 День {day} пока недоступен. Сначала завершите предыдущий день.")
    
    @dp.callback_query_handler(lambda c: c.data.startswith("day_") and c.data.endswith("_start"))
    async def start_day(callback_query: types.CallbackQuery):
        """Начинает или продолжает день адаптации"""
        user_id = callback_query.from_user.id
        day = int(callback_query.data.split("_")[1])
        
        # Проверка доступа с учетом 24ч задержки
        if not progress_manager.is_admin(user_id):
            progress = progress_manager.get_user_progress(user_id)
            # Если предыдущий день не завершен — блокируем
            if day > 1:
                prev_status = progress.get("day_progress", {}).get(f"day_{day-1}", {}).get("status")
                if prev_status != "completed":
                    await callback_query.message.answer("🔒 Этот день пока недоступен. Сначала завершите предыдущий день.")
                    return
            # Если день еще locked — возможно, не истекло время
            cur_status = progress.get("day_progress", {}).get(f"day_{day}", {}).get("status", "locked")
            if cur_status == "locked":
                remaining = progress_manager.get_remaining_wait_time(user_id, day)
                if remaining is not None and remaining > 0:
                    hours = remaining // 3600
                    minutes = (remaining % 3600) // 60
                    await callback_query.message.answer(
                        f"⏳ Этот день будет доступен через {hours}ч {minutes}м. Пожалуйста, возвращайтесь позже."
                    )
                else:
                    await callback_query.message.answer("🔒 Этот день пока недоступен. Пожалуйста, возвращайтесь позже.")
                return

        # Помечаем день как начатый (для доступных/завершенных тоже обновим started_at при первом входе)
        progress_manager.mark_day_started(user_id, day)
        
        # Для Дня 2 показываем вступление и кнопку Старт
        if day == 2:
            intro = (
                "Рад видеть тебя! Сегодня второй день Адаптационной программы.\n"
                "Сегодня мы пойдём чуть глубже — не в карьер, а в саму душу нашей команды.\n\n"
                "Тебя ждёт:\n"
                "– Знакомство с корпоративными ценностями (включи ролик и почувствуй атмосферу нашей компании)\n"
                "– Корпоративные компетенции (смотри ролик и отметь, что тебе особенно близко)\n"
                "– Вводный инструктаж (знания, которые сделают твою работу безопасной и уверенной)\n\n"
                "Помни, каждый шаг адаптации — это кирпичик в твой фундамент успеха в «Беш Арча».\n"
                "Ну что, готов? Тогда нажимай «Старт» и вперёд!\n"
                "Поставь стикер Арчи – Так держать!"
            )
            try:
                await callback_query.message.answer_sticker(GOOD_JOB_STICKER_ID)
            except:
                pass
            await callback_query.message.answer(intro, reply_markup=day2_intro_keyboard())
            return

        # Для Дня 4 — своё вступление
        if day == 4:
            from handlers.mission import day4_start
            await day4_start(callback_query)
            return

        # Для дня 1 запускаем поток сразу с приветствия CEO
        if day == 1:
            from handlers.ceo_greeting import start_ceo_greeting
            await start_ceo_greeting(callback_query.message, user_id)
            return
        # Для дня 3 запускаем сразу вводный блок
        if day == 3:
            from handlers.mission import day3_start
            await day3_start(callback_query)
            return

        # Для остальных дней показываем меню модулей
        await callback_query.message.answer(
            f"📅 *День {day} адаптации*\n\nВыберите модуль для изучения:",
            reply_markup=smart_day_menu_keyboard(user_id, day),
            parse_mode='Markdown'
        )
    
    @dp.callback_query_handler(lambda c: c.data.startswith("module_"))
    async def handle_module(callback_query: types.CallbackQuery):
        """Обрабатывает выбор модуля"""
        user_id = callback_query.from_user.id
        parts = callback_query.data.split("_")
        day = int(parts[1])
        module = "_".join(parts[2:-1])  # Модуль может содержать подчеркивания
        
        # Проверяем доступ к модулю
        if not progress_manager.can_access_day(user_id, day):
            await callback_query.message.answer("🔒 Этот модуль пока недоступен.")
            return
        
        # Перенаправляем на соответствующий обработчик
        if module == "Приветствие от Генерального директора":
            from handlers.ceo_greeting import start_ceo_greeting
            await start_ceo_greeting(callback_query.message, user_id)
        elif module == "Легенда компании":
            from handlers.legend import start_legend_module
            await start_legend_module(user_id, callback_query.message)
        elif module == "Современная история":
            from handlers.modern_history import start_modern_history_module
            await start_modern_history_module(callback_query.message, user_id)
        elif module == "Корпоративные ценности":
            from handlers.mission import values_ack
            await values_ack(callback_query)
        elif module == "Корпоративные компетенции":
            from handlers.mission import competencies_ack
            await competencies_ack(callback_query)
        elif module == "Вводный инструктаж":
            from handlers.mission import briefing_ack
            await briefing_ack(callback_query)
        else:
            await callback_query.message.answer(f"📚 Модуль '{module}' находится в разработке...")
    
    # Обработчик "О компании" реализован в handlers/company_info.py