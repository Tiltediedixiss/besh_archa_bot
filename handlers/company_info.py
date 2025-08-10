from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.company_info_keyboard import company_info_keyboard, corporate_culture_keyboard
from keyboards.main_menu import start_next_day_keyboard
from data.progress import progress_manager
from data.files import CORPORATE_ETHICS_PDF_PATH
import os


def register_company_info(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data == "company_info")
    async def company_info(callback_query: types.CallbackQuery):
        # Сформируем media group из 3 изображений (как в новостях), с предварительным сжатием
        photo_paths = ["data/1.jpg", "data/2.jpg", "data/3.jpg"]
        media_group = []
        import io
        try:
            from PIL import Image
            for path in photo_paths:
                if not os.path.exists(path):
                    continue
                with Image.open(path) as im:
                    im = im.convert("RGB")
                    width, height = im.size
                    max_side = 1600
                    scale = min(1.0, max_side / max(width, height))
                    if scale < 1.0:
                        new_size = (int(width * scale), int(height * scale))
                        im = im.resize(new_size, Image.LANCZOS)
                    buf = io.BytesIO()
                    im.save(buf, format="JPEG", quality=85, optimize=True)
                    buf.seek(0)
                    media_group.append(types.InputMediaPhoto(types.InputFile(buf, filename=os.path.basename(path))))
            if media_group:
                await callback_query.message.answer_media_group(media_group)
        except Exception:
            # Если не удалось собрать группу (или нет Pillow), отправим по одному с безопасным падением
            max_photo_bytes = 10 * 1024 * 1024
            for path in photo_paths:
                if not os.path.exists(path):
                    continue
                try:
                    file_size = os.path.getsize(path)
                    if file_size > max_photo_bytes:
                        with open(path, "rb") as f:
                            await callback_query.message.answer_document(types.InputFile(f, filename=os.path.basename(path)))
                    else:
                        with open(path, "rb") as f:
                            await callback_query.message.answer_photo(types.InputFile(f))
                except Exception:
                    try:
                        with open(path, "rb") as f:
                            await callback_query.message.answer_document(types.InputFile(f, filename=os.path.basename(path)))
                    except Exception:
                        pass
        # Сообщение с ссылкой на полный альбом
        await callback_query.message.answer(
            "Ознакомься с нашими сотрудниками — команда, руководство и атмосфера компании.\n"
            "Больше фотографий: https://disk.yandex.kz/d/ro9clH4yB1jhTQ"
        )
        # Предложение продолжить адаптацию в соответствии с прогрессом
        user_id = callback_query.from_user.id
        next_day = progress_manager.get_next_available_day(user_id)
        await callback_query.message.answer(
            "Готов продолжить адаптационную программу?",
            reply_markup=start_next_day_keyboard(next_day)
        )

    @dp.callback_query_handler(lambda c: c.data == "corporate_culture")
    async def corporate_culture(callback_query: types.CallbackQuery):
        await callback_query.message.answer(
            "📚 Корпоративная культура\n\nЗдесь вы можете ознакомиться с Кодексом корпоративной этики компании 'Беш Арча'.",
            reply_markup=corporate_culture_keyboard()
        )

    @dp.callback_query_handler(lambda c: c.data == "download_corporate_ethics")
    async def send_corporate_ethics_pdf(callback_query: types.CallbackQuery):
        if os.path.exists(CORPORATE_ETHICS_PDF_PATH):
            with open(CORPORATE_ETHICS_PDF_PATH, "rb") as pdf:
                await callback_query.message.answer_document(
                    pdf,
                    caption="Кодекс корпоративной этики компании 'Беш Арча' (PDF)"
                )
        else:
            await callback_query.message.answer("❗️Файл не найден. Пожалуйста, обратитесь к HR.")
        # После отправки файла показываем клавиатуру снова
        await callback_query.message.answer(
            "Хотите ознакомиться с брендбуком компании?",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Перейти к Брендбуку", callback_data="brandbook"),
                types.InlineKeyboardButton("⬅️ В меню документов", callback_data="org_docs")
            )
        ) 