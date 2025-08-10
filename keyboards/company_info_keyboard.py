from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def company_info_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("👤 Первые шаги в компании", callback_data="ceo_greeting"),
        InlineKeyboardButton("🤖 Легенда о Бель-Алма", callback_data="legend_start"),
        InlineKeyboardButton("📝 Адаптационная программа", callback_data="adapt_program"),
        InlineKeyboardButton("🎯 Цели на испытательный срок", callback_data="trial_goals"),
        InlineKeyboardButton("📚 Корпоративная культура", callback_data="corporate_culture"),
        InlineKeyboardButton("📑 Организационные документы", callback_data="org_docs"),
        InlineKeyboardButton("📰 Новости компании", callback_data="news_block"),
        InlineKeyboardButton("⬅️ Вернуться", callback_data="main_menu"),
    )
    return kb

def corporate_culture_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📥 Скачать Кодекс корпоративной этики (PDF)", callback_data="download_corporate_ethics"),
        InlineKeyboardButton("⬅️ Назад", callback_data="company_info")
    )
    return kb 