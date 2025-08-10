from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.progress import progress_manager

def start_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Да, поехали", callback_data="ceo_greeting"),
        InlineKeyboardButton("Позже", callback_data="later")
    )
    return kb

def ceo_greeting_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Дальше", callback_data="legend_start"))
    return kb

def legend_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Да, расскажи!", callback_data="legend_next_1"))
    return kb

def legend_next_keyboard(step, total):
    kb = InlineKeyboardMarkup()
    if step < total - 2:
        kb.add(InlineKeyboardButton("Дальше", callback_data=f"legend_next_{step+1}"))
    elif step == total - 2:
        kb.add(InlineKeyboardButton("Современная история", callback_data="modern_history"))
    return kb

def modern_history_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Дальше", callback_data="video_legend_offer"))
    return kb

def legend_to_modern_history_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Современная история", callback_data="modern_history"))
    return kb

def main_menu_keyboard(user_id: int = None):
    """Умная главная клавиатура, которая учитывает прогресс пользователя"""
    kb = InlineKeyboardMarkup(row_width=2)
    
    # Базовые разделы, доступные всегда
    kb.add(InlineKeyboardButton("📊 Мой прогресс", callback_data="show_progress"))
    kb.add(InlineKeyboardButton("ℹ️ О компании", callback_data="company_info"))
    
    # Если передан user_id, проверяем прогресс
    if user_id:
        progress = progress_manager.get_user_progress(user_id)
        current_day = progress.get("current_day", 1)
        
        # Проверяем, является ли пользователь админом
        is_admin = progress_manager.is_admin(user_id)
        
        # Показываем доступные дни
        for day in range(1, 5):
            day_key = f"day_{day}"
            if day_key in progress["day_progress"]:
                status = progress["day_progress"][day_key]["status"]
                
                if status == "completed":
                    kb.add(InlineKeyboardButton(f"✅ День {day} (Завершен)", callback_data=f"day_{day}_start"))
                elif status in ["in_progress", "available"]:
                    kb.add(InlineKeyboardButton(f"🔄 День {day}", callback_data=f"day_{day}_start"))
                elif is_admin:
                    # Админы видят все дни, даже заблокированные
                    kb.add(InlineKeyboardButton(f"🔒 День {day}", callback_data=f"day_{day}_start"))
                # Обычные пользователи не видят заблокированные дни
    
    # Если user_id не передан, показываем стандартное меню
    else:
        kb.add(InlineKeyboardButton("🏛️ Легенда", callback_data="legend"))
        kb.add(InlineKeyboardButton("📜 Современная история", callback_data="modern_history"))
        kb.add(InlineKeyboardButton("🎯 Миссия и ценности", callback_data="mission"))
        kb.add(InlineKeyboardButton("👨‍💼 Приветствие CEO", callback_data="ceo_greeting"))
        kb.add(InlineKeyboardButton("📰 Новости", callback_data="news"))
        kb.add(InlineKeyboardButton("📋 Важные документы", callback_data="important_docs"))
    
    return kb

def smart_day_menu_keyboard(user_id: int, day: int):
    """Клавиатура для конкретного дня с учетом прогресса"""
    kb = InlineKeyboardMarkup(row_width=1)
    
    progress = progress_manager.get_user_progress(user_id)
    day_key = f"day_{day}"
    
    if day_key in progress["day_progress"]:
        day_data = progress["day_progress"][day_key]
        completed_modules = day_data["completed_modules"]
        
        # Показываем модули дня
        from data.texts import ADAPTATION_PROGRAM
        if day_key in ADAPTATION_PROGRAM:
            for module in ADAPTATION_PROGRAM[day_key]["modules"]:
                if module in completed_modules:
                    kb.add(InlineKeyboardButton(f"✅ {module}", callback_data=f"module_{day}_{module}_start"))
                else:
                    kb.add(InlineKeyboardButton(f"📚 {module}", callback_data=f"module_{day}_{module}_start"))
    
    # Кнопки навигации - только для админов
    if progress_manager.is_admin(user_id):
        kb.add(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    
    if day > 1:
        prev_day_status = progress["day_progress"].get(f"day_{day-1}", {}).get("status", "locked")
        if prev_day_status in ["completed", "available", "in_progress"] or progress_manager.is_admin(user_id):
            kb.add(InlineKeyboardButton("⬅️ Предыдущий день", callback_data=f"day_{day-1}_start"))
    
    if day < 4:
        next_day_status = progress["day_progress"].get(f"day_{day+1}", {}).get("status", "locked")
        if next_day_status in ["available", "in_progress"] or progress_manager.is_admin(user_id):
            kb.add(InlineKeyboardButton("➡️ Следующий день", callback_data=f"day_{day+1}_start"))
    
    return kb

def today_plan_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Показать чек-лист на первый день", callback_data="show_checklist"))
    return kb

def start_next_day_keyboard(next_day: int):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(f"🚀 Начать день {next_day}", callback_data=f"day_{next_day}_start"))
    return kb

def video_legend_keyboard(user_id: int = None):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("🇷🇺 Русский язык", callback_data="video_legend_russian"))
    kb.add(InlineKeyboardButton("🇰🇬 Кыргыз тили", callback_data="video_legend_kyrgyz"))
    kb.add(InlineKeyboardButton("Пропустить", callback_data="skip_videos"))
    
    # Кнопка "Главное меню" только для админов
    if user_id:
        if progress_manager.is_admin(user_id):
            kb.add(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    
    return kb

def day_completion_keyboard(user_id: int = None):
    """Клавиатура для завершения дня с кнопкой 'Главное меню' только для админов"""
    kb = InlineKeyboardMarkup(row_width=1)
    
    # Кнопка "Главное меню" только для админов
    if user_id:
        if progress_manager.is_admin(user_id):
            kb.add(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))
    
    return kb 