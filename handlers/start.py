from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.main_menu import main_menu_keyboard
from data.progress import progress_manager
from data.files import ARCHI_STICKER_ID

def register_start(dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def start_command(message: types.Message):
        """Обработчик команды /start"""
        user_id = message.from_user.id
        # Сохраняем username/имя/фамилию для отчетов
        progress_manager.update_user_profile(
            user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        
        # Инициализируем прогресс для нового пользователя
        progress_manager.get_user_progress(user_id)
        
        # Сначала отправляем приветственный стикер от Арчи
        try:
            await message.answer_sticker(ARCHI_STICKER_ID)
        except:
            await message.answer("👋 Привет от Арчи!")
        
        welcome_text = (
            "🏠 *Добро пожаловать в адаптационный бот компании «Беш Арча»!*\n\n"
            "Я Арчи, ваш помощник по адаптации. Мы пройдем 4-дневную программу знакомства с компанией.\n\n"
            "📚 *Что вас ждет:*\n"
            "• День 1: Знакомство с компанией\n"
            "• День 2: Корпоративная культура и правила\n"
            "• День 3: Профессиональное развитие\n"
            "• День 4: Интеграция в команду\n\n"
            "🚀 Начнем с первого дня?"
        )
        
        await message.answer(welcome_text, 
                           reply_markup=main_menu_keyboard(user_id),
                           parse_mode='Markdown')
    
    @dp.message_handler(commands=["help"])
    async def help_command(message: types.Message):
        """Обработчик команды /help"""
        help_text = (
            "📖 *Доступные команды:*\n\n"
            "/start - Начать адаптацию\n"
            "/progress - Показать ваш прогресс\n"
            "/next_day - Информация о следующем дне\n"
            "/help - Показать эту справку\n\n"
            "💡 *Советы:*\n"
            "• Проходите модули по порядку\n"
            "• Каждый день разблокируется после завершения предыдущего\n"
            "• Используйте кнопки навигации для удобства\n"
            "• Если что-то не ясно - не стесняйтесь спрашивать!"
        )
        
        await message.answer(help_text, parse_mode='Markdown') 