import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
import os
from typing import Dict, List, Any
from .progress import progress_manager

class ExcelExporter:
    """Класс для экспорта данных о прогрессе пользователей в Excel"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Создает директорию для отчетов, если она не существует"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def export_user_progress(self, filename: str = None) -> str:
        """Экспортирует прогресс всех пользователей в Excel файл"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"user_progress_report_{timestamp}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Получаем данные о прогрессе всех пользователей
        all_progress = self._get_all_user_progress()
        
        # Создаем Excel файл
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Основная таблица прогресса
            self._create_main_progress_sheet(writer, all_progress)
            
            # Детальная таблица по модулям
            self._create_modules_detail_sheet(writer, all_progress)
            
            # Статистика по дням
            self._create_days_statistics_sheet(writer, all_progress)
            
            # Сводка по завершению
            self._create_completion_summary_sheet(writer, all_progress)
        
        return filepath
    
    def _get_all_user_progress(self) -> List[Dict[str, Any]]:
        """Получает прогресс всех пользователей"""
        return progress_manager.get_all_users_progress()
    
    def _create_main_progress_sheet(self, writer: pd.ExcelWriter, data: List[Dict[str, Any]]):
        """Создает основной лист с прогрессом пользователей"""
        if not data:
            # Создаем заглушку для демонстрации
            df = pd.DataFrame({
                'User ID': [123456789, 987654321],
                'Username': ['user1', 'user2'],
                'First Name': ['Иван', 'Мария'],
                'Last Name': ['Иванов', 'Петрова'],
                'Current Day': [1, 2],
                'Day 1 Status': ['completed', 'completed'],
                'Day 2 Status': ['locked', 'in_progress'],
                'Day 3 Status': ['locked', 'locked'],
                'Day 4 Status': ['locked', 'locked'],
                'Total Modules Completed': [3, 4],
                'Last Activity': ['2024-01-15 10:30', '2024-01-15 14:20'],
                'Is Admin': [False, False]
            })
        else:
            # Используем реальные данные
            df = pd.DataFrame(data)
        
        df.to_excel(writer, sheet_name='Основной прогресс', index=False)
        
        # Применяем стили
        self._apply_main_sheet_styling(writer.sheets['Основной прогресс'])
    
    def _create_modules_detail_sheet(self, writer: pd.ExcelWriter, data: List[Dict[str, Any]]):
        """Создает детальный лист по модулям"""
        # Получаем детальные данные по модулям
        modules_data = progress_manager.get_modules_detail_data()
        
        if not modules_data:
            # Создаем заглушку для демонстрации
            df = pd.DataFrame({
                'User ID': [123456789, 123456789, 123456789, 987654321, 987654321],
                'Username': ['user1', 'user1', 'user1', 'user2', 'user2'],
                'Day': [1, 1, 1, 1, 2],
                'Module': ['Приветствие от CEO', 'Легенда компании', 'Современная история', 'Приветствие от CEO', 'Миссия и ценности'],
                'Status': ['completed', 'completed', 'completed', 'completed', 'in_progress'],
                'Completion Date': ['2024-01-15 09:15', '2024-01-15 09:45', '2024-01-15 10:30', '2024-01-15 14:00', '2024-01-15 14:20'],
                'Time Spent (min)': [5, 15, 10, 5, 8]
            })
        else:
            # Используем реальные данные
            df = pd.DataFrame(modules_data)
        
        df.to_excel(writer, sheet_name='Детали по модулям', index=False)
        
        # Применяем стили
        self._apply_modules_sheet_styling(writer.sheets['Детали по модулям'])
    
    def _create_days_statistics_sheet(self, writer: pd.ExcelWriter, data: List[Dict[str, Any]]):
        """Создает лист со статистикой по дням"""
        # Получаем статистику по дням
        days_stats = progress_manager.get_days_statistics()
        
        if not days_stats:
            # Создаем заглушку для демонстрации
            df = pd.DataFrame({
                'Day': [1, 2, 3, 4],
                'Total Users': [2, 1, 0, 0],
                'Completed': [2, 0, 0, 0],
                'In Progress': [0, 1, 0, 0],
                'Locked': [0, 1, 2, 2],
                'Completion Rate (%)': [100.0, 0.0, 0.0, 0.0],
                'Average Time (min)': [30.0, 0.0, 0.0, 0.0]
            })
        else:
            # Используем реальные данные
            df = pd.DataFrame(days_stats)
        
        df.to_excel(writer, sheet_name='Статистика по дням', index=False)
        
        # Применяем стили
        self._apply_statistics_sheet_styling(writer.sheets['Статистика по дням'])
    
    def _create_completion_summary_sheet(self, writer: pd.ExcelWriter, data: List[Dict[str, Any]]):
        """Создает лист со сводкой по завершению"""
        # Получаем сводку по завершению
        completion_summary = progress_manager.get_completion_summary()
        
        if not completion_summary:
            # Создаем заглушку для демонстрации
            summary_data = {
                'Metric': [
                    'Общее количество пользователей',
                    'Пользователи, завершившие День 1',
                    'Пользователи, завершившие День 2',
                    'Пользователи, завершившие День 3',
                    'Пользователи, завершившие День 4',
                    'Пользователи, завершившие всю программу',
                    'Среднее время прохождения Дня 1',
                    'Среднее время прохождения всей программы',
                    'Процент отсева после Дня 1',
                    'Процент отсева после Дня 2'
                ],
                'Value': [
                    2,
                    2,
                    0,
                    0,
                    0,
                    0,
                    '30 мин',
                    '0 мин',
                    '0%',
                    '0%'
                ],
                'Notes': [
                    'Активные пользователи в системе',
                    '100% пользователей',
                    'Пока никто не начал',
                    'День заблокирован',
                    'День заблокирован',
                    'Пока никто не завершил',
                    'Включая все модули',
                    'Пока не применимо',
                    'Все пользователи продолжают',
                    'Все пользователи продолжают'
                ]
            }
            df = pd.DataFrame(summary_data)
        else:
            # Используем реальные данные
            df = pd.DataFrame(completion_summary)
        
        df.to_excel(writer, sheet_name='Сводка по завершению', index=False)
        
        # Применяем стили
        self._apply_summary_sheet_styling(writer.sheets['Сводка по завершению'])
    
    def _apply_main_sheet_styling(self, worksheet):
        """Применяет стили к основному листу"""
        # Заголовки
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Автоматическая ширина колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def _apply_modules_sheet_styling(self, worksheet):
        """Применяет стили к листу модулей"""
        # Заголовки
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Автоматическая ширина колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def _apply_statistics_sheet_styling(self, worksheet):
        """Применяет стили к листу статистики"""
        # Заголовки
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="C5504B", end_color="C5504B", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Автоматическая ширина колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def _apply_summary_sheet_styling(self, worksheet):
        """Применяет стили к листу сводки"""
        # Заголовки
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Автоматическая ширина колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

# Создаем глобальный экземпляр экспортера
excel_exporter = ExcelExporter() 