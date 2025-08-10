from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.progress import progress_manager

def register_progress(dp: Dispatcher):
    @dp.message_handler(commands=['progress'])
    async def show_progress(message: types.Message):
        """Показывает прогресс пользователя по адаптации"""
        user_id = message.from_user.id
        progress_summary = progress_manager.get_progress_summary(user_id)
        
        # Добавляем информацию о следующем доступном дне
        next_day = progress_manager.get_next_available_day(user_id)
        if next_day > 1:
            progress_summary += f"\n🎯 *Следующий доступный день:* {next_day}"
        
        await message.reply(progress_summary, parse_mode='Markdown')
    
    @dp.message_handler(commands=['reset_progress'])
    async def reset_progress(message: types.Message):
        """Сбрасывает прогресс пользователя (только для админов)"""
        user_id = message.from_user.id
        
        # Проверяем, является ли пользователь админом
        from main import ADMIN_ID
        if user_id == ADMIN_ID:
            progress_manager.reset_user_progress(user_id)
            await message.reply("✅ Прогресс пользователя сброшен. Теперь можно начать заново.")
        else:
            await message.reply("❌ У вас нет прав для сброса прогресса.")
    
    @dp.message_handler(commands=['check_admin'])
    async def check_admin(message: types.Message):
        """Проверяет статус администратора пользователя"""
        user_id = message.from_user.id
        
        if progress_manager.is_admin(user_id):
            await message.reply("✅ Вы являетесь администратором! У вас есть доступ ко всем дням.")
        else:
            await message.reply("❌ Вы не являетесь администратором.")
    
    @dp.message_handler(commands=['force_admin_update'])
    async def force_admin_update(message: types.Message):
        """Принудительно обновляет доступ админа ко всем дням"""
        user_id = message.from_user.id
        
        if progress_manager.is_admin(user_id):
            progress_manager.force_update_admin_access(user_id)
            await message.reply("✅ Доступ админа ко всем дням обновлен! Теперь вы можете видеть все 4 дня.")
        else:
            await message.reply("❌ Эта команда доступна только администраторам.")
    
    @dp.message_handler(commands=['next_day'])
    async def next_day_info(message: types.Message):
        """Показывает информацию о следующем доступном дне"""
        user_id = message.from_user.id
        next_day = progress_manager.get_next_available_day(user_id)
        
        from data.texts import ADAPTATION_PROGRAM
        day_key = f"day_{next_day}"
        
        if day_key in ADAPTATION_PROGRAM:
            day_info = ADAPTATION_PROGRAM[day_key]
            modules = "\n".join([f"• {module}" for module in day_info["modules"]])
            
            response = f"📅 *{day_info['title']}*\n\n"
            response += f"🎯 *Модули для изучения:*\n{modules}\n\n"
            
            if next_day == 1:
                response += "🚀 Начинаем адаптацию! Выберите первый модуль в главном меню."
            else:
                response += f"🔓 Этот день станет доступен после завершения дня {next_day - 1}."
            
            await message.reply(response, parse_mode='Markdown')
        else:
            await message.reply("❌ Информация о дне не найдена.") 