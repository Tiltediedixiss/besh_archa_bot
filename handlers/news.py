from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.news_keyboard import news_keyboard

# file_id для трёх фото (замени на свои)
NEWS_PHOTOS = [
    "AgACAgIAAxkBAAIBmmhzhIe_BRApXtWtUUdNvdN9UHDfAAIw-TEbL7qhS8t0lmCDR-4jAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIBmGhzhIG1HCbNhR9U8Ikv7HfQtnyRAAIa6zEbXvygS4lV3gABvRU0gQEAAwIAA3kAAzYE",
    "AgACAgIAAxkBAAIBlmhzhHtmGMpLc39ebxrPoBmN_sB2AAIZ6zEbXvygS1O_SlRgiWrJAQADAgADeQADNgQ",
]

def register_news(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "news_block")
    async def news_block(callback_query: types.CallbackQuery):
        text = (
            "📰 <b>Новости компании</b>\n\n"
            "Мы недавно провели Стратсессию 2025! 📈✨\n"
            "Посмотри фото и видео с нашего мероприятия 👇"
        )
        # Отправляем текст
        await callback_query.message.answer(text, parse_mode="HTML")
        # Отправляем 3 фото в одном сообщении (media group)
        media = [types.InputMediaPhoto(photo) for photo in NEWS_PHOTOS]
        await callback_query.message.answer_media_group(media)
        # Кнопки
        await callback_query.message.answer("Выбери, что посмотреть:", reply_markup=news_keyboard()) 