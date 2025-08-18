from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.excel_exporter import excel_exporter
from data.progress import progress_manager
import os

def register_excel_export(dp: Dispatcher):
    @dp.message_handler(commands=["export_progress"])
    async def export_progress_command(message: types.Message):
        """Обработчик команды /export_progress для экспорта данных в Excel"""
        user_id = message.from_user.id
        
        # Проверяем, является ли пользователь админом
        if not progress_manager.is_admin(user_id):
            await message.answer("❌ У вас нет прав для экспорта данных. Эта команда доступна только администраторам.")
            return
        
        try:
            # Отправляем сообщение о начале экспорта
            status_msg = await message.answer("📊 Начинаю экспорт данных о прогрессе пользователей...")
            
            # Экспортируем данные в Excel
            filepath = excel_exporter.export_user_progress()
            
            # Отправляем файл
            with open(filepath, 'rb') as file:
                await message.answer_document(
                    file,
                    caption="📈 Отчет о прогрессе пользователей готов!\n\n"
                           "Файл содержит:\n"
                           "• Основной прогресс всех пользователей\n"
                           "• Детали по модулям\n"
                           "• Статистику по дням\n"
                           "• Сводку по завершению программы"
                )
            
            # Удаляем временное сообщение о статусе
            await status_msg.delete()
            
            # Удаляем временный файл
            try:
                os.remove(filepath)
            except:
                pass  # Игнорируем ошибки при удалении
                
        except Exception as e:
            await message.answer(f"❌ Ошибка при экспорте данных: {str(e)}")
    
    @dp.message_handler(commands=["clean_reports"])
    async def clean_reports_command(message: types.Message):
        """Удаляет все временные XLSX из папки reports (только для админов)."""
        user_id = message.from_user.id
        if not progress_manager.is_admin(user_id):
            await message.answer("❌ У вас нет прав для этой операции.")
            return

        reports_dir = "reports"
        if not os.path.isdir(reports_dir):
            await message.answer("📁 Папка reports отсутствует — очищать нечего.")
            return

        removed = 0
        for name in os.listdir(reports_dir):
            if name.lower().endswith(".xlsx"):
                path = os.path.join(reports_dir, name)
                try:
                    os.remove(path)
                    removed += 1
                except Exception:
                    pass

        await message.answer(f"🧹 Удалено файлов: {removed}")

    @dp.message_handler(commands=["export_feedbacks"])
    async def export_feedbacks_command(message: types.Message):
        """Отправляет файл feedback_day4.csv администраторам."""
        user_id = message.from_user.id
        if not progress_manager.is_admin(user_id):
            await message.answer("❌ У вас нет прав для экспорта. Команда доступна только администраторам.")
            return

        csv_path = "feedback_day4.csv"
        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            await message.answer("📭 Отзывы отсутствуют: файл feedback_day4.csv пуст или не найден.")
            return

        try:
            with open(csv_path, 'rb') as f:
                await message.answer_document(f, caption="Отзывы пользователей (CSV)")
        except Exception as e:
            await message.answer(f"❌ Не удалось отправить файл: {str(e)}")

    @dp.message_handler(commands=["progress_stats"])
    async def progress_stats_command(message: types.Message):
        """Обработчик команды /progress_stats для просмотра статистики"""
        user_id = message.from_user.id
        
        # Проверяем, является ли пользователь админом
        if not progress_manager.is_admin(user_id):
            await message.answer("❌ У вас нет прав для просмотра статистики. Эта команда доступна только администраторам.")
            return
        
        try:
            # Получаем краткую статистику
            all_progress = progress_manager.get_all_users_progress()
            total_users = len(all_progress)
            
            if total_users == 0:
                await message.answer("📊 Статистика:\n\nПока нет данных о пользователях.")
                return
            
            # Подсчитываем статистику (используем реальные ключи из get_all_users_progress)
            day1_completed = sum(1 for user in all_progress if user.get('Day 1 Status') == 'completed')
            day2_completed = sum(1 for user in all_progress if user.get('Day 2 Status') == 'completed')
            day3_completed = sum(1 for user in all_progress if user.get('Day 3 Status') == 'completed')
            day4_completed = sum(1 for user in all_progress if user.get('Day 4 Status') == 'completed')
            
            admins = sum(1 for user in all_progress if user.get('Is Admin', False))
            
            # Экранируем проценты для Markdown и избегаем проблем с сущностями
            d1p = f"{day1_completed/total_users*100:.1f}%".replace('%', '\\%')
            d2p = f"{day2_completed/total_users*100:.1f}%".replace('%', '\\%')
            d3p = f"{day3_completed/total_users*100:.1f}%".replace('%', '\\%')
            d4p = f"{day4_completed/total_users*100:.1f}%".replace('%', '\\%')

            stats_text = (
                "📊 Статистика прогресса пользователей:\n\n"
                f"👥 Общее количество пользователей: {total_users}\n"
                f"👑 Администраторов: {admins}\n\n"
                "📅 Прогресс по дням:\n"
                f"• День 1: {day1_completed}/{total_users} ({d1p})\n"
                f"• День 2: {day2_completed}/{total_users} ({d2p})\n"
                f"• День 3: {day3_completed}/{total_users} ({d3p})\n"
                f"• День 4: {day4_completed}/{total_users} ({d4p})\n\n"
                "💡 Используйте /export_progress для получения детального отчета в Excel"
            )

            await message.answer(stats_text)
            
        except Exception as e:
            await message.answer(f"❌ Ошибка при получении статистики: {str(e)}") 