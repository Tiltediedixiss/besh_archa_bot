from aiogram import types
from aiogram.dispatcher import Dispatcher

def register_get_file_id(dp: Dispatcher):
    @dp.message_handler(commands=['get_file_id'])
    async def get_file_id_command(message: types.Message):
        await message.reply(
            "Отправьте мне любой файл (фото, стикер, документ, видео, аудио), "
            "и я покажу вам его file_id.\n\n"
            "Это нужно для настройки бота."
        )
    
    @dp.message_handler(content_types=['photo'])
    async def get_photo_id(message: types.Message):
        await message.reply(f"file_id: {message.photo[-1].file_id}")
    
    @dp.message_handler(content_types=['sticker'])
    async def get_sticker_id(message: types.Message):
        await message.reply(f"file_id стикера: {message.sticker.file_id}")
    
    @dp.message_handler(content_types=['document'])
    async def get_document_id(message: types.Message):
        await message.reply(f"file_id документа: {message.document.file_id}")
    
    @dp.message_handler(content_types=['video'])
    async def get_video_id(message: types.Message):
        await message.reply(f"file_id видео: {message.video.file_id}")
    
    @dp.message_handler(content_types=['audio'])
    async def get_audio_id(message: types.Message):
        await message.reply(f"file_id аудио: {message.audio.file_id}") 