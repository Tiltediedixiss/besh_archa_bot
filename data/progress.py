import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

PROGRESS_FILE = "data/user_progress.json"

# ID администратора (замените на ваш реальный Telegram ID)
ADMIN_ID = 2092094721  # Замените на ваш ID

class UserProgress:
    def __init__(self):
        self.progress_file = PROGRESS_FILE
        self.ensure_progress_file()
    
    def ensure_progress_file(self):
        """Создает файл прогресса, если он не существует"""
        os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)
        if not os.path.exists(self.progress_file):
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
    
    def get_user_progress(self, user_id: int) -> Dict:
        """Получает прогресс пользователя и актуализирует разблокировки по времени."""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_progress = {}

        user_id_str = str(user_id)
        user_progress = all_progress.get(user_id_str, self.get_default_progress(user_id))

        # Если пользователь админ, убеждаемся что все дни доступны
        if self.is_admin(user_id):
            user_progress = self.ensure_admin_access(user_progress)
        else:
            # Актуализируем тайм-локи и разблокировки для обычного пользователя
            changed = self._refresh_unlocks_in_user_progress(user_progress)
            if changed:
                all_progress[user_id_str] = user_progress
                self.save_progress(all_progress)

        return user_progress
    
    def get_default_progress(self, user_id: int = None) -> Dict:
        """Возвращает прогресс по умолчанию для нового пользователя"""
        # Для админов все дни доступны
        if user_id and self.is_admin(user_id):
            return {
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "username": None,
                "first_name": None,
                "last_name": None,
                "current_day": 1,
                "completed_modules": [],
                "day_progress": {
                    "day_1": {
                        "status": "available",
                        "completed_modules": [],
                        "started_at": datetime.now().isoformat(),
                        "completed_at": None,
                        "unlocked_at": None
                    },
                    "day_2": {
                        "status": "available",
                        "completed_modules": [],
                        "started_at": datetime.now().isoformat(),
                        "completed_at": None,
                        "unlocked_at": None
                    },
                    "day_3": {
                        "status": "available",
                        "completed_modules": [],
                        "started_at": datetime.now().isoformat(),
                        "completed_at": None,
                        "unlocked_at": None
                    },
                    "day_4": {
                        "status": "available",
                        "completed_modules": [],
                        "started_at": datetime.now().isoformat(),
                        "completed_at": None,
                        "unlocked_at": None
                    }
                }
            }
        else:
            # Для обычных пользователей только первый день доступен
            return {
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "username": None,
                "first_name": None,
                "last_name": None,
                "current_day": 1,
                "completed_modules": [],
                "day_progress": {
                    "day_1": {
                        "status": "in_progress",
                        "completed_modules": [],
                        "started_at": datetime.now().isoformat(),
                        "completed_at": None,
                        "unlocked_at": None
                    },
                    "day_2": {
                        "status": "locked",
                        "completed_modules": [],
                        "started_at": None,
                        "completed_at": None,
                        "unlocked_at": None
                    },
                    "day_3": {
                        "status": "locked",
                        "completed_modules": [],
                        "started_at": None,
                        "completed_at": None,
                        "unlocked_at": None
                    },
                    "day_4": {
                        "status": "locked",
                        "completed_modules": [],
                        "started_at": None,
                        "completed_at": None,
                        "unlocked_at": None
                    }
                }
            }
    
    def update_module_progress(self, user_id: int, module_name: str, day: int = 1):
        """Обновляет прогресс по модулю для конкретного пользователя.
        ВАЖНО: здесь работаем со всем файлом прогресса, а не только с прогрессом пользователя."""
        # Загружаем весь прогресс из файла
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_progress = {}

        user_id_str = str(user_id)
        user_progress = all_progress.get(user_id_str, self.get_default_progress(user_id))

        # Добавляем модуль в завершенные на уровне пользователя
        if module_name not in user_progress.get("completed_modules", []):
            user_progress.setdefault("completed_modules", []).append(module_name)

        # Обновляем прогресс дня
        day_key = f"day_{day}"
        day_progress = user_progress.setdefault("day_progress", {})
        if day_key in day_progress:
            day_data = day_progress[day_key]
            day_data.setdefault("completed_modules", [])
            if module_name not in day_data["completed_modules"]:
                day_data["completed_modules"].append(module_name)

            # Проверяем, завершен ли день
            day_modules = self.get_day_modules(day)
            if len(day_data["completed_modules"]) >= len(day_modules):
                # Отмечаем завершение дня
                now_iso = datetime.now().isoformat()
                day_data["status"] = "completed"
                day_data["completed_at"] = now_iso

                # Планируем разблокировку следующего дня через 24 часа (только для обычных пользователей)
                if day < 4:
                    next_day_key = f"day_{day + 1}"
                    if next_day_key in day_progress:
                        unlock_time = datetime.now() + timedelta(hours=24)
                        day_progress[next_day_key]["unlocked_at"] = unlock_time.isoformat()
                        # Статус оставляем locked до наступления времени

        # Сохраняем изменения обратно в общий файл
        all_progress[user_id_str] = user_progress
        self.save_progress(all_progress)
    
    def update_user_profile(self, user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str]):
        """Сохраняет username/имя/фамилию пользователя в файле прогресса"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_progress = {}
        user_id_str = str(user_id)
        user_progress = all_progress.get(user_id_str, self.get_default_progress(user_id))
        if username:
            user_progress["username"] = username
        if first_name:
            user_progress["first_name"] = first_name
        if last_name:
            user_progress["last_name"] = last_name
        all_progress[user_id_str] = user_progress
        self.save_progress(all_progress)
    
    def get_day_modules(self, day: int) -> List[str]:
        """Возвращает модули для конкретного дня"""
        from data.texts import ADAPTATION_PROGRAM
        day_key = f"day_{day}"
        if day_key in ADAPTATION_PROGRAM:
            return ADAPTATION_PROGRAM[day_key]["modules"]
        return []
    
    def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь администратором"""
        return user_id == ADMIN_ID

    def _refresh_unlocks_in_user_progress(self, user_progress: Dict) -> bool:
        """Проверяет таймеры разблокировки и открывает дни, если время пришло."""
        changed = False
        day_prog = user_progress.get("day_progress", {})
        for day in range(2, 5):
            key = f"day_{day}"
            if key not in day_prog:
                continue
            status = day_prog[key].get("status", "locked")
            if status != "locked":
                continue
            unlocked_at = day_prog[key].get("unlocked_at")
            if unlocked_at:
                try:
                    dt_unlock = datetime.fromisoformat(unlocked_at)
                    if datetime.now() >= dt_unlock:
                        day_prog[key]["status"] = "available"
                        changed = True
                except Exception:
                    # Игнорируем некорректные форматы дат
                    pass
        return changed

    def get_remaining_wait_time(self, user_id: int, day: int) -> Optional[int]:
        """Возвращает оставшееся время ожидания (в секундах) до разблокировки дня, либо None."""
        progress = self.get_user_progress(user_id)
        day_key = f"day_{day}"
        day_data = progress.get("day_progress", {}).get(day_key, {})
        unlocked_at = day_data.get("unlocked_at")
        if not unlocked_at:
            return None
        try:
            dt_unlock = datetime.fromisoformat(unlocked_at)
            remaining = (dt_unlock - datetime.now()).total_seconds()
            return int(remaining) if remaining > 0 else 0
        except Exception:
            return None

    def mark_day_started(self, user_id: int, day: int) -> None:
        """Помечает день как начатый: выставляет started_at и переводит доступный день в in_progress."""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_progress = {}

        user_id_str = str(user_id)
        user_progress = all_progress.get(user_id_str, self.get_default_progress(user_id))
        day_key = f"day_{day}"
        day_data = user_progress.setdefault("day_progress", {}).setdefault(day_key, {
            "status": "in_progress",
            "completed_modules": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "unlocked_at": None,
        })

        if not day_data.get("started_at"):
            day_data["started_at"] = datetime.now().isoformat()
        if day_data.get("status") == "available":
            day_data["status"] = "in_progress"

        all_progress[user_id_str] = user_progress
        self.save_progress(all_progress)
    
    def ensure_admin_access(self, user_progress: Dict) -> Dict:
        """Обеспечивает админу доступ ко всем дням"""
        if "day_progress" in user_progress:
            for day in range(1, 5):
                day_key = f"day_{day}"
                if day_key in user_progress["day_progress"]:
                    user_progress["day_progress"][day_key]["status"] = "available"
                    if user_progress["day_progress"][day_key]["started_at"] is None:
                        user_progress["day_progress"][day_key]["started_at"] = datetime.now().isoformat()
        
        return user_progress
    
    def force_update_admin_access(self, user_id: int):
        """Принудительно обновляет доступ админа ко всем дням"""
        if not self.is_admin(user_id):
            return
        
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
            
            user_id_str = str(user_id)
            if user_id_str in progress:
                user_progress = progress[user_id_str]
                updated_progress = self.ensure_admin_access(user_progress)
                progress[user_id_str] = updated_progress
                self.save_progress(progress)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    def can_access_day(self, user_id: int, day: int) -> bool:
        """Проверяет, может ли пользователь получить доступ к дню (учитывая 24ч задержку)."""
        # Админы имеют доступ ко всем дням
        if self.is_admin(user_id):
            return True

        progress = self.get_user_progress(user_id)
        if day == 1:
            return True

        # Для остальных дней: предыдущий день должен быть завершен
        prev_day_key = f"day_{day - 1}"
        prev_completed = progress.get("day_progress", {}).get(prev_day_key, {}).get("status") == "completed"
        if not prev_completed:
            return False

        # Текущий день не должен быть заблокирован
        cur_status = progress.get("day_progress", {}).get(f"day_{day}", {}).get("status", "locked")
        return cur_status != "locked"
    
    def get_next_available_day(self, user_id: int) -> int:
        """Возвращает следующий доступный день"""
        progress = self.get_user_progress(user_id)
        
        for day in range(1, 5):
            day_key = f"day_{day}"
            if day_key in progress["day_progress"]:
                status = progress["day_progress"][day_key]["status"]
                if status in ["in_progress", "available"]:
                    return day
        
        return 1
    
    def save_progress(self, progress: Dict):
        """Сохраняет прогресс в файл"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    
    def reset_user_progress(self, user_id: int):
        """Сбрасывает прогресс пользователя"""
        # Загружаем весь прогресс
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_progress = {}

        user_id_str = str(user_id)
        all_progress[user_id_str] = self.get_default_progress(user_id)
        self.save_progress(all_progress)
    
    def get_progress_summary(self, user_id: int) -> str:
        """Возвращает сводку прогресса пользователя"""
        user_progress = self.get_user_progress(user_id)
        
        summary = "📊 *Ваш прогресс по адаптации:*\n\n"
        
        for day in range(1, 5):
            day_key = f"day_{day}"
            if day_key in user_progress["day_progress"]:
                day_data = user_progress["day_progress"][day_key]
                status = day_data["status"]
                completed_count = len(day_data["completed_modules"])
                total_modules = len(self.get_day_modules(day))
                
                if status == "completed":
                    summary += f"✅ День {day}: Завершен ({completed_count}/{total_modules})\n"
                elif status == "in_progress":
                    summary += f"🔄 День {day}: В процессе ({completed_count}/{total_modules})\n"
                elif status == "available":
                    summary += f"🔓 День {day}: Доступен\n"
                else:
                    summary += f"🔒 День {day}: Заблокирован\n"
        
        return summary
    
    def get_all_users_progress(self) -> List[Dict[str, Any]]:
        """Возвращает прогресс всех пользователей для HR-отчетов"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        result = []
        for user_id_str, user_progress in all_progress.items():
            # Пропускаем невалидные записи
            try:
                uid = int(user_id_str)
            except (ValueError, TypeError):
                continue
            if not isinstance(user_progress, dict):
                continue
            
            # Подсчитываем статистику
            total_modules = 0
            current_day = 1
            
            for day in range(1, 5):
                day_key = f"day_{day}"
                if isinstance(user_progress.get("day_progress"), dict) and day_key in user_progress["day_progress"]:
                    day_data = user_progress["day_progress"][day_key]
                    total_modules += len(day_data["completed_modules"])
                    
                    if day_data["status"] == "completed":
                        current_day = day + 1
                    elif day_data["status"] == "in_progress":
                        current_day = day
            
            # Определяем статус каждого дня
            day_statuses = {}
            for day in range(1, 5):
                day_key = f"day_{day}"
                if day_key in user_progress["day_progress"]:
                    day_statuses[f"Day {day} Status"] = user_progress["day_progress"][day_key]["status"]
                else:
                    day_statuses[f"Day {day} Status"] = "locked"
            
            # Формируем запись пользователя
            user_record = {
                "User ID": uid,
                "Username": user_progress.get("username") or "Не указано",
                "First Name": user_progress.get("first_name") or "Не указано",
                "Last Name": user_progress.get("last_name") or "Не указано",
                "Current Day": current_day,
                "Total Modules Completed": total_modules,
                "Last Activity": user_progress.get("last_activity", "Не указано"),
                "Is Admin": self.is_admin(uid),
                **day_statuses
            }
            
            result.append(user_record)
        
        return result
    
    def get_modules_detail_data(self) -> List[Dict[str, Any]]:
        """Возвращает детальные данные по модулям для HR-отчетов"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        result = []
        for user_id_str, user_progress in all_progress.items():
            # Пропускаем невалидные записи
            try:
                uid = int(user_id_str)
            except (ValueError, TypeError):
                continue
            if not isinstance(user_progress, dict):
                continue
            
            for day in range(1, 5):
                day_key = f"day_{day}"
                if day_key in user_progress["day_progress"]:
                    day_data = user_progress["day_progress"][day_key]
                    
                    for module in day_data["completed_modules"]:
                        module_record = {
                            "User ID": uid,
                            "Username": user_progress.get("username") or "Не указано",
                            "Day": day,
                            "Module": module,
                            "Status": "completed",
                            "Completion Date": day_data.get("started_at", "Не указано"),
                            "Time Spent (min)": 15  # Примерное время, можно расширить для точного учета
                        }
                        result.append(module_record)
        
        return result
    
    def get_days_statistics(self) -> List[Dict[str, Any]]:
        """Возвращает статистику по дням для HR-отчетов"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Учитываем только валидные пользовательские записи (ключ — числовой user_id)
        valid_progress = [v for k, v in all_progress.items() if str(k).isdigit() and isinstance(v, dict)]
        total_users = len(valid_progress)
        if total_users == 0:
            return []
        
        result = []
        for day in range(1, 5):
            completed = 0
            in_progress = 0
            locked = 0
            
            for user_progress in valid_progress:
                if not isinstance(user_progress, dict) or "day_progress" not in user_progress:
                    locked += 1
                    continue
                day_key = f"day_{day}"
                if day_key in user_progress["day_progress"]:
                    status = user_progress["day_progress"][day_key]["status"]
                    if status == "completed":
                        completed += 1
                    elif status == "in_progress":
                        in_progress += 1
                    else:
                        locked += 1
                else:
                    locked += 1
            
            completion_rate = (completed / total_users * 100) if total_users > 0 else 0
            avg_time = 30 if completed > 0 else 0  # Примерное время, можно расширить
            
            day_stats = {
                "Day": day,
                "Total Users": total_users,
                "Completed": completed,
                "In Progress": in_progress,
                "Locked": locked,
                "Completion Rate (%)": round(completion_rate, 1),
                "Average Time (min)": avg_time
            }
            result.append(day_stats)
        
        return result
    
    def get_completion_summary(self) -> List[Dict[str, Any]]:
        """Возвращает сводку по завершению для HR-отчетов"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Учитываем только валидные пользовательские записи (ключ — числовой user_id)
        valid_progress = [v for k, v in all_progress.items() if str(k).isdigit() and isinstance(v, dict)]
        total_users = len(valid_progress)
        if total_users == 0:
            return []
        
        # Подсчитываем статистику
        day1_completed = 0
        day2_completed = 0
        day3_completed = 0
        day4_completed = 0
        all_completed = 0
        
        for user_progress in valid_progress:
            if not isinstance(user_progress, dict) or "day_progress" not in user_progress:
                continue
            for day in range(1, 5):
                day_key = f"day_{day}"
                if day_key in user_progress["day_progress"]:
                    if user_progress["day_progress"][day_key]["status"] == "completed":
                        if day == 1:
                            day1_completed += 1
                        elif day == 2:
                            day2_completed += 1
                        elif day == 3:
                            day3_completed += 1
                        elif day == 4:
                            day4_completed += 1
        
        # Проверяем, кто завершил всю программу
        for user_progress in valid_progress:
            if not isinstance(user_progress, dict) or "day_progress" not in user_progress:
                continue
            all_days_completed = True
            for day in range(1, 5):
                day_key = f"day_{day}"
                if day_key not in user_progress["day_progress"] or \
                   user_progress["day_progress"][day_key]["status"] != "completed":
                    all_days_completed = False
                    break
            if all_days_completed:
                all_completed += 1
        
        # Рассчитываем проценты отсева
        dropout_after_day1 = ((total_users - day1_completed) / total_users * 100) if total_users > 0 else 0
        dropout_after_day2 = ((day1_completed - day2_completed) / day1_completed * 100) if day1_completed > 0 else 0
        
        summary_data = {
            "Metric": [
                "Общее количество пользователей",
                "Пользователи, завершившие День 1",
                "Пользователи, завершившие День 2",
                "Пользователи, завершившие День 3",
                "Пользователи, завершившие День 4",
                "Пользователи, завершившие всю программу",
                "Среднее время прохождения Дня 1",
                "Среднее время прохождения всей программы",
                "Процент отсева после Дня 1",
                "Процент отсева после Дня 2"
            ],
            "Value": [
                total_users,
                day1_completed,
                day2_completed,
                day3_completed,
                day4_completed,
                all_completed,
                "30 мин",
                "120 мин",
                f"{round(dropout_after_day1, 1)}%",
                f"{round(dropout_after_day2, 1)}%"
            ],
            "Notes": [
                "Активные пользователи в системе",
                f"{round(day1_completed/total_users*100, 1)}% пользователей" if total_users > 0 else "0%",
                f"{round(day2_completed/day1_completed*100, 1)}% от завершивших День 1" if day1_completed > 0 else "0%",
                f"{round(day3_completed/day2_completed*100, 1)}% от завершивших День 2" if day2_completed > 0 else "0%",
                f"{round(day4_completed/day3_completed*100, 1)}% от завершивших День 3" if day3_completed > 0 else "0%",
                f"{round(all_completed/total_users*100, 1)}% от всех пользователей" if total_users > 0 else "0%",
                "Включая все модули",
                "Примерное время для полного прохождения",
                f"{total_users - day1_completed} пользователей не завершили День 1",
                f"{day1_completed - day2_completed} пользователей не завершили День 2"
            ]
        }
        
        return [summary_data]

# Глобальный экземпляр для использования в других модулях
progress_manager = UserProgress() 