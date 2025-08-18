import csv
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.mission_keyboard import (
    day2_intro_keyboard,
    values_watch_keyboard,
    values_ack_keyboard,
    competencies_basic_watch_keyboard,
    competencies_basic_ack_keyboard,
    competencies_mgmt_watch_keyboard,
    competencies_mgmt_ack_keyboard,
    briefing_watch_keyboard,
    briefing_ack_keyboard,
    day3_intro_keyboard,
    day3_after_video_keyboard,
    day3_rules_keyboard,
    day3_faq_menu_keyboard,
    day3_faq_back_keyboard,
    day4_intro_keyboard,
    day4_ethics_ack_keyboard,
    day4_brandbook_keyboard,
    day4_brandbook_ack_keyboard,
    day4_news_keyboard,
    day4_docs_keyboard,
    day4_referral_keyboard,
    day4_feedback_keyboard,
)
from keyboards.important_docs_keyboard import important_docs_keyboard
from keyboards.company_info_keyboard import corporate_culture_keyboard
from data.files import CORPORATE_ETHICS_PDF_PATH, GOOD_JOB_STICKER_ID, INSTRUCTIONS_PDF_PATH, ASK_QUESTION_STICKER_ID, SAFETY_FIRST_STICKER_ID, DAY3_FAREWELL_STICKER_ID, RULES_IMAGE_PATH, BRANDBOOK_PDF_PATH
import os

# День 2: ссылки на ролики (YouTube превью)
VALUES_VIDEO_URL = "https://youtu.be/dClTK79sweQ"
COMPETENCIES_BASIC_VIDEO_URL = "https://youtu.be/jA3w7bzUMeo"  # Основные компетенции (временно тот же ролик)
COMPETENCIES_MGMT_VIDEO_URL = "https://youtu.be/aMrCd1itH7U"   # Управленческие компетенции

CSV_FILE = "mission_ack.csv"

class MissionState(StatesGroup):
    language = State()

def register_mission(dp: Dispatcher):
    # День 2 — вступление от Арчи
    @dp.callback_query_handler(lambda c: c.data == "day_2_start")
    async def day2_entry(callback_query: types.CallbackQuery):
        text = (
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
        await callback_query.message.answer(text, reply_markup=day2_intro_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "day2_start")
    async def day2_start(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "Ознаокмься видеороликом о Корпоративных ценностях нашей Компании", reply_markup=values_watch_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "values_video")
    async def values_video(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📺 Корпоративные ценности — ролик:\n" + VALUES_VIDEO_URL
        )
        await callback_query.message.answer(
            "Когда посмотрите ролик, нажмите «Я ознакомлен».",
            reply_markup=values_ack_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "values_ack")
    async def values_ack(callback_query: types.CallbackQuery):
        # Отмечаем модуль как завершенный
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Корпоративные ценности", 2)
        await callback_query.message.answer(
            "Отлично! Переходим к следующему блоку: Корпоративные компетенции"
        )
        await callback_query.message.answer(
            "Сначала посмотрим ролик про Основные компетенции.",
            reply_markup=competencies_basic_watch_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "competencies_video_basic")
    async def competencies_video_basic(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📺 Основные компетенции — ролик:\n" + COMPETENCIES_BASIC_VIDEO_URL
        )
        await callback_query.message.answer(
            "После просмотра нажмите «Я ознакомлен».",
            reply_markup=competencies_basic_ack_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "competencies_basic_ack")
    async def competencies_basic_ack(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "Теперь посмотрим ролик про Управленческие компетенции.",
            reply_markup=competencies_mgmt_watch_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "competencies_video_mgmt")
    async def competencies_video_mgmt(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📺 Управленческие компетенции — ролик:\n" + COMPETENCIES_MGMT_VIDEO_URL
        )
        await callback_query.message.answer(
            "После просмотра нажмите «Я ознакомлен».",
            reply_markup=competencies_mgmt_ack_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "competencies_mgmt_ack")
    async def competencies_mgmt_ack(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Корпоративные компетенции", 2)
        await callback_query.message.answer(
            "Отлично! Переходим к заключительному блоку второго дня: Вводный инструктаж.",
            reply_markup=briefing_watch_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "briefing_start")
    async def briefing_start(callback_query: types.CallbackQuery):
        # Отправляем PDF с вводным инструктажем
        import os
        if os.path.exists(INSTRUCTIONS_PDF_PATH):
            with open(INSTRUCTIONS_PDF_PATH, 'rb') as doc:
                await callback_query.message.answer_document(
                    doc,
                    caption="📄 Вводный инструктаж (PDF)"
                )
        else:
            await callback_query.message.answer("❗️Файл инструктажа не найден. Пожалуйста, обратитесь к HR.")
        await callback_query.message.answer(
            "После ознакомления нажмите «Я ознакомлен».",
            reply_markup=briefing_ack_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "briefing_ack")
    async def briefing_ack(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Вводный инструктаж", 2)
        # Финальное сообщение дня 2 + стикер
        farewell = (
            "Отлично! \n"
            "Ты уже познакомился с нашими ценностями и корпоративными компетенциями.\n"
            "Теперь ты знаешь, что «Беш Арча» — это не только уголь и техника, но и команда, где каждый важен, где ценят безопасность, ответственность и готовность помогать друг другу.\n"
            "Эти принципы — наш внутренний компас. Держи его при себе в любой ситуации, и он всегда приведёт тебя к правильным решениям.\n"
            "📞 Важно: если что-то не ясно — не бойся спрашивать. Мы здесь, чтобы помочь. До завтра! "
        )
        try:
            await callback_query.message.answer_sticker(ASK_QUESTION_STICKER_ID)
        except:
            pass
        await callback_query.message.answer(farewell)

    # ===== День 3 =====
    @dp.callback_query_handler(lambda c: c.data == "day_3_start")
    async def day3_start(callback_query: types.CallbackQuery):
        intro = (
            "Рад видеть тебя! Сегодня третий день Адаптационной программы.\n\n"
            "Сегодня говорим о самом важном — безопасности на работе и бытовых вопросах.\n"
            "⚠️ Промышленная безопасность — главное. Инструктаж — это защита тебя, твоих коллег и оборудования."
        )
        await callback_query.message.answer(intro, reply_markup=day3_intro_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "day3_watch_video")
    async def day3_watch_video(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "🎥 Видеоинструктаж скоро будет доступен. Кнопка активируется, как только добавим ссылку."
        )
        try:
            await callback_query.message.answer_sticker(SAFETY_FIRST_STICKER_ID)
        except:
            pass
        await callback_query.message.answer(
            "📍 Помни: каска, спецодежда, техника безопасности — не формальность. Это то, что сохраняет здоровье и жизнь.",
            reply_markup=day3_after_video_keyboard()
        )
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Видеоинструктаж", 3)

    @dp.callback_query_handler(lambda c: c.data == "day3_rules")
    async def day3_rules(callback_query: types.CallbackQuery):
        # Отправляем изображение памятки с напоминанием и кнопкой "Дальше" для перехода к FAQ
        import os
        if os.path.exists(RULES_IMAGE_PATH):
            with open(RULES_IMAGE_PATH, 'rb') as img:
                await callback_query.message.answer_photo(
                    img,
                    caption=(
                        "📍 Помни: каска, спецодежда, техника безопасности — не формальность. "
                        "Это то, что сохраняет здоровье и жизнь."
                    ),
                    reply_markup=day3_rules_keyboard()
                )
        else:
            await callback_query.message.answer(
                "📍 Помни: каска, спецодежда, техника безопасности — не формальность. "
                "Это то, что сохраняет здоровье и жизнь.",
                reply_markup=day3_rules_keyboard()
            )
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Памятка 10 правил", 3)

    @dp.callback_query_handler(lambda c: c.data == "day3_download_rules")
    async def day3_download_rules(callback_query: types.CallbackQuery):
        # Больше не используется — оставлено на случай старых callback'ов
        await day3_faq(callback_query)

    @dp.callback_query_handler(lambda c: c.data == "day3_faq")
    async def day3_faq(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "Выбери интересующий вопрос — отвечу коротко и по делу 👇",
            reply_markup=day3_faq_menu_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data.startswith("day3_faq_"))
    async def day3_faq_item(callback_query: types.CallbackQuery):
        mapping = {
            "day3_faq_loc": (
                "📍 Где находится разрез и как добраться?\n"
                "Разрез «Беш Арча» расположен в ___ (координаты). Добраться можно на корпоративном автобусе (расписание по ссылке) или личным авто через КПП №1."
            ),
            "day3_faq_schedule": (
                "⏰ Какой график работы?\n"
                "Смены — день/ночь по 12 часов, офис — с 09:00 до 18:00, пн–пт."
            ),
            "day3_faq_pass": (
                "🪪 Как оформить пропуск?\n"
                "Через отдел безопасности после инструктажа и медосмотра."
            ),
            "day3_faq_gear": (
                "👕 Где получить спецодежду?\n"
                "На складе СИЗ №___ по направлению отдела охраны труда."
            ),
            "day3_faq_canteen": (
                "🍲 Есть ли столовая?\n"
                "Да, работает по графику."
            ),
            "day3_faq_housing": (
                "🏢 Жильё для сотрудников\n"
                "Для вахтовиков — комнаты на 2–4 человека в вахтовом посёлке."
            ),
            "day3_faq_med": (
                "🩺 Медпункт\n"
                "Медпункт расположен на территории вахтового поселка."
            ),
            "day3_faq_contacts": (
                "🩺 Наши контакты:\n"
                "+996 773 433 343\n"
                "info@besharcha.kg\n"
                "Головной офис\n"
                "Кыргызстан, Бишкек, Первомайский р-н, ул. Панфилова, д. 178, каб. 805 (8-й этаж)"
            ),
        }
        text = mapping.get(callback_query.data, "")
        if text:
            await callback_query.message.answer(text, reply_markup=day3_faq_back_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "day3_finish")
    async def day3_finish(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "FAQ и контакты", 3)
        farewell = (
            "Ну что, друг, третий день — позади! \n"
            "Сегодня ты узнал, как всё устроено у нас в «Беш Арча» — где живём, как добираемся, где поесть, где отдохнуть и к кому обращаться, если нужна помощь.\n\n"
            "Логистика и быт — это фундамент, который помогает нам работать с комфортом и без лишних забот.\n\n"
            "Впереди новые знания и новые знакомства.\n\n"
            "До завтра, твой Арчи! \n"
        )
        try:
            await callback_query.message.answer_sticker(DAY3_FAREWELL_STICKER_ID)
        except:
            pass
        await callback_query.message.answer(farewell)

    # ===== День 4 =====
    @dp.callback_query_handler(lambda c: c.data == "day_4_start")
    async def day4_start(callback_query: types.CallbackQuery):
        text = (
            "Рад видеть тебя! Сегодня четвертый день Адаптационной программы.\n\n"
            "Мы откроем для тебя ещё одну важную часть жизни «Беш Арча» — нашу культуру и атмосферу.\n"
            "Здесь ты узнаешь, что делает нас не просто коллегами, а командой, которая поддерживает друг друга и идёт к целям вместе.\n\n"
            "🤝 У нас принято:\n"
            "– Поддерживать друг друга\n"
            "– Быть честными\n"
            "– Работать на результат\n"
            "– Помнить, что мы — команда"
        )
        await callback_query.message.answer(text, reply_markup=day4_intro_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "day4_ethics")
    async def day4_ethics(callback_query: types.CallbackQuery):
        # Отправляем PDF кодекса и кнопку "Я ознакомлен"
        if os.path.exists(CORPORATE_ETHICS_PDF_PATH):
            with open(CORPORATE_ETHICS_PDF_PATH, "rb") as pdf:
                await callback_query.message.answer_document(
                    pdf, caption="Кодекс корпоративной этики (PDF)"
                )
        else:
            await callback_query.message.answer("❗️Файл кодекса не найден.")
        await callback_query.message.answer(
            "Нажми «Я ознакомлен», когда изучишь документ.",
            reply_markup=day4_ethics_ack_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "day4_ethics_ack")
    async def day4_ethics_ack(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Кодекс корпоративной этики", 4)
        await callback_query.message.answer(
            "Отлично! Теперь давай посмотрим брендбук компании.",
            reply_markup=day4_brandbook_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "day4_brandbook")
    async def day4_brandbook(callback_query: types.CallbackQuery):
        if os.path.exists(BRANDBOOK_PDF_PATH):
            with open(BRANDBOOK_PDF_PATH, "rb") as pdf:
                await callback_query.message.answer_document(
                    pdf, caption="Брендбук компании (PDF)"
                )
        else:
            await callback_query.message.answer("❗️Файл брендбука не найден.")
        await callback_query.message.answer(
            "Когда будешь готов — нажми «Я ознакомлен».",
            reply_markup=day4_brandbook_ack_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "day4_brandbook_ack")
    async def day4_brandbook_ack(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Брендбук", 4)
        await callback_query.message.answer(
            "О новостях и событиях Компании у нас есть раздел. Можешь часто туда заглядывать.",
            reply_markup=day4_news_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "day4_docs")
    async def day4_docs(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Новости и события", 4)
        await callback_query.message.answer(
            "В разделе «Важные документы» ты найдёшь оргструктуру, коллективный договор и другое (PDF).",
            reply_markup=day4_docs_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "day4_referral")
    async def day4_referral(callback_query: types.CallbackQuery):
        from data.progress import progress_manager
        progress_manager.update_module_progress(callback_query.from_user.id, "Важные документы", 4)
        progress_manager.update_module_progress(callback_query.from_user.id, "Реферальная программа", 4)
        text = (
            "Сегодня заключительный день Адаптационной программы. За эти дни ты узнал, как устроен «Беш Арча» — от ценностей и правил безопасности до быта, логистики и нашей корпоративной атмосферы.\n"
            "Ты уже знаешь, где работать, к кому обращаться, как защитить себя на смене и как стать частью нашей команды.\n"
            "Но самое главное — ты стал ближе к людям, с которыми теперь будешь двигаться вперёд.\n\n"
            "Сегодня я расскажу тебе о реферальной программе.\n\n"
            "📌 Как это работает:\n"
            "— Отправь реферальную ссылку или передай контакт человека в HR-боте.\n"
            "— Если кандидат проходит собеседование и выходит на работу — ты получаешь бонус.\n\n"
            "🏆 Участие в конкурсе лучших рекомендателей\n\n"
            "🔍 Кого мы ищем? (смотри раздел Вакансии)"
        )
        await callback_query.message.answer(text, reply_markup=day4_referral_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "vacancies_info")
    async def vacancies_info(callback_query: types.CallbackQuery):
        await callback_query.message.answer("Раздел вакансий в разработке. Обратитесь в HR для актуального списка.")

    @dp.callback_query_handler(lambda c: c.data == "day4_feedback")
    async def day4_feedback(callback_query: types.CallbackQuery):
        text = (
            "Нам важно знать, как прошла твоя адаптация.\n"
            "Что было полезным? Что можно улучшить?\n"
            "Поделись впечатлением — это поможет сделать программу ещё лучше.\n\n"
            "📝 Напиши, пожалуйста:\n"
            "• Что тебе понравилось в сопровождении чат-бота?\n"
            "• Что вызвало трудности или осталось непонятным?\n"
            "• Какие функции или шаги ты бы добавил?"
        )
        await callback_query.message.answer(text, reply_markup=day4_feedback_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "day4_feedback_start")
    async def day4_feedback_start(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Напишите ваш отзыв одним сообщением, я его передам HR.")
        await state.set_state("waiting_feedback")

    @dp.message_handler(state="waiting_feedback")
    async def day4_feedback_collect(message: types.Message, state: FSMContext):
        # Сохраним в CSV для простоты
        with open("feedback_day4.csv", "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([message.from_user.id, message.from_user.full_name, message.text, datetime.now().isoformat()])
        from data.progress import progress_manager
        progress_manager.update_module_progress(message.from_user.id, "Отзыв об адаптации", 4)
        await message.answer(
            "🎉 Поздравляю, ты прошёл адаптационную программу!\n"
            "Теперь ты — часть нашей команды 💛\n"
            "Пусть каждый день здесь приносит тебе смысл, стабильность и уважение.\n"
            "По вопросам жалоб и предложений: info@besharcha.kg"
        )
        await state.finish()