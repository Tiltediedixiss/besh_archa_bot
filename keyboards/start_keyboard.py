from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Да, поехали", callback_data="ceo_greeting"),
        InlineKeyboardButton("Позже, в Главное меню", callback_data="main_menu")
    )
    return kb 