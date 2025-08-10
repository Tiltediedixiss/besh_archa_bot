from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# День 2: клавиатуры

def day2_intro_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Старт", callback_data="day2_start"))
    return kb

# Блок «Ценности»
def values_watch_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📺 Смотреть ролик", callback_data="values_video"))
    return kb

def values_ack_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("✅ Я ознакомлен", callback_data="values_ack"))
    return kb

# Блок «Компетенции» — два ролика
def competencies_basic_watch_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📺 Основные компетенции", callback_data="competencies_video_basic"))
    return kb

def competencies_basic_ack_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("✅ Я ознакомлен", callback_data="competencies_basic_ack"))
    return kb

def competencies_mgmt_watch_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📺 Управленческие компетенции", callback_data="competencies_video_mgmt"))
    return kb

def competencies_mgmt_ack_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("✅ Я ознакомлен", callback_data="competencies_mgmt_ack"))
    return kb

# Блок «Вводный инструктаж»
def briefing_watch_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📄 Скачать инструктаж (PDF)", callback_data="briefing_start"))
    return kb

def briefing_ack_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("✅ Я ознакомлен", callback_data="briefing_ack"))
    return kb

# День 3: клавиатуры
def day3_intro_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Смотреть видеоинструктаж", callback_data="day3_watch_video"))
    return kb

def day3_after_video_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Дальше", callback_data="day3_rules"))
    return kb

def day3_rules_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("➡️ Дальше", callback_data="day3_faq"))
    return kb

def day3_faq_menu_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📍 Где находится разрез?", callback_data="day3_faq_loc"))
    kb.add(InlineKeyboardButton("⏰ График работы", callback_data="day3_faq_schedule"))
    kb.add(InlineKeyboardButton("🪪 Пропуск", callback_data="day3_faq_pass"))
    kb.add(InlineKeyboardButton("👕 Спецодежда", callback_data="day3_faq_gear"))
    kb.add(InlineKeyboardButton("🍲 Столовая", callback_data="day3_faq_canteen"))
    kb.add(InlineKeyboardButton("🏢 Жильё", callback_data="day3_faq_housing"))
    kb.add(InlineKeyboardButton("🩺 Медпункт", callback_data="day3_faq_med"))
    kb.add(InlineKeyboardButton("📞 Контакты", callback_data="day3_faq_contacts"))
    kb.add(InlineKeyboardButton("➡️ Дальше", callback_data="day3_finish"))
    return kb

def day3_faq_back_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад к FAQ", callback_data="day3_faq"),
        InlineKeyboardButton("➡️ Дальше", callback_data="day3_finish"),
    )
    return kb

# ===== День 4 =====
def day4_intro_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Познакомиться с Кодексом корпоративной этики", callback_data="day4_ethics"))
    return kb

def day4_ethics_ack_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Я ознакомлен", callback_data="day4_ethics_ack"))
    return kb

def day4_brandbook_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Ознакомиться с Брендбуком Компании", callback_data="day4_brandbook"))
    return kb

def day4_brandbook_ack_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Я ознакомлен", callback_data="day4_brandbook_ack"))
    return kb

def day4_news_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Открыть Новости Компании", callback_data="news_block"),
        InlineKeyboardButton("Дальше", callback_data="day4_docs")
    )
    return kb

def day4_docs_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Открыть раздел Важные документы", callback_data="important_docs"),
        InlineKeyboardButton("Дальше", callback_data="day4_referral")
    )
    return kb

def day4_referral_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Вакансии", callback_data="vacancies_info"),
        InlineKeyboardButton("Дальше", callback_data="day4_feedback")
    )
    return kb

def day4_feedback_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("🔘 Хочу оставить отзыв", callback_data="day4_feedback_start"))
    return kb