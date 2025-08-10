from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def news_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Фото", url="https://drive.google.com/drive/folders/18k_xW0mX3CNJrzPxTDMndqPhUlKCIaye?usp=sharing"))
    kb.add(InlineKeyboardButton("Видео", url="https://drive.google.com/drive/folders/18k_xW0mX3CNJrzPxTDMndqPhUlKCIaye?usp=sharing"))
    kb.add(InlineKeyboardButton("Дальше", callback_data="day4_docs"))
    return kb 