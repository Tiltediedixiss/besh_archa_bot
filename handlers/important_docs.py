from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.important_docs_keyboard import important_docs_keyboard, back_to_docs_keyboard
from keyboards.mission_keyboard import (
    competencies_basic_watch_keyboard,
    competencies_mgmt_watch_keyboard,
)
from handlers.mission import VALUES_VIDEO_URL
from handlers.mission import COMPETENCIES_BASIC_VIDEO_URL, COMPETENCIES_MGMT_VIDEO_URL
from data.files import RULES_IMAGE_PATH
from data.files import BRANDBOOK_PDF_PATH
import os

def register_important_docs(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "important_docs")
    async def important_docs(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📄 Важные документы. Выберите интересующий раздел:",
            reply_markup=important_docs_keyboard()
        )

    # Корпоративные ценности (ссылка на видео)
    @dp.callback_query_handler(lambda c: c.data == "important_values")
    async def important_values(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📺 Корпоративные ценности — ролик:\n" + VALUES_VIDEO_URL,
            reply_markup=back_to_docs_keyboard()
        )

    # Ролики о компетенциях — два видео
    @dp.callback_query_handler(lambda c: c.data == "important_competencies")
    async def important_competencies(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📺 Основные компетенции — ролик:\n" + COMPETENCIES_BASIC_VIDEO_URL
        )
        await callback_query.message.answer(
            "📺 Управленческие компетенции — ролик:\n" + COMPETENCIES_MGMT_VIDEO_URL,
            reply_markup=back_to_docs_keyboard()
        )

    # Памятка 10 правил — показать изображение и текст-памятку
    @dp.callback_query_handler(lambda c: c.data == "important_rules")
    async def important_rules(callback_query: types.CallbackQuery):
        if os.path.exists(RULES_IMAGE_PATH):
            with open(RULES_IMAGE_PATH, 'rb') as img:
                await callback_query.message.answer_photo(
                    img,
                    caption=(
                        "📍 Помни: каска, спецодежда, техника безопасности — не формальность. "
                        "Это то, что сохраняет здоровье и жизнь."
                    )
                )
        else:
            await callback_query.message.answer(
                "📍 Помни: каска, спецодежда, техника безопасности — не формальность. Это то, что сохраняет здоровье и жизнь."
            )
        await callback_query.message.answer(
            "Готово. Вернуться может по кнопке ниже.",
            reply_markup=back_to_docs_keyboard()
        )

    # Организационная структура — показать одну картинку structure.png
    @dp.callback_query_handler(lambda c: c.data == "important_structure")
    async def important_structure(callback_query: types.CallbackQuery):
        path = os.path.join("data", "structure.png")
        if os.path.exists(path):
            with open(path, 'rb') as img:
                await callback_query.message.answer_photo(img, caption="Организационная структура")
        else:
            await callback_query.message.answer("❗️Файл структуры не найден.")
        await callback_query.message.answer("Вернуться назад:", reply_markup=back_to_docs_keyboard())

    @dp.callback_query_handler(lambda c: c.data == "brandbook")
    async def send_brandbook_pdf(callback_query: types.CallbackQuery):
        if os.path.exists(BRANDBOOK_PDF_PATH):
            with open(BRANDBOOK_PDF_PATH, "rb") as pdf:
                await callback_query.message.answer_document(
                    pdf,
                    caption="Брендбук компании 'Беш Арча' (PDF)"
                )
        else:
            await callback_query.message.answer("❗️Файл брендбука не найден. Пожалуйста, обратитесь к HR.")
        await callback_query.message.answer(
            "Вы можете вернуться назад или скачать брендбук снова:",
            reply_markup=important_docs_keyboard()
        ) 