from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def important_docs_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💠 Корпоративные ценности", callback_data="important_values"),
        InlineKeyboardButton("🎬 Ролики о компетенциях", callback_data="important_competencies"),
        InlineKeyboardButton("🏛️ Организационная структура", callback_data="important_structure"),
        InlineKeyboardButton("📝 Памятка 10 правил", callback_data="important_rules"),
        InlineKeyboardButton("📘 Брендбук компании", callback_data="brandbook"),
        InlineKeyboardButton("➡️ Дальше", callback_data="day4_referral"),
    )
    return kb

def back_to_docs_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("⬅️ Назад к важным документам", callback_data="important_docs"))
    return kb