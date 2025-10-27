#!/usr/bin/env python3
"""
Упрощенное ядро системы CREATOR
Работает без внешних зависимостей
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

class MemoryLevel:
    """Уровень памяти"""
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.data = {}
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Создает директорию если не существует"""
        os.makedirs(self.path, exist_ok=True)
    
    def update(self, data: Dict[str, Any]):
        """Обновляет данные уровня"""
        self.data.update(data)
        self._save()
    
    def _save(self):
        """Сохраняет данные в файл"""
        file_path = os.path.join(self.path, f"{self.name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def load(self):
        """Загружает данные из файла"""
        file_path = os.path.join(self.path, f"{self.name}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        return self.data

class FourLevelMemory:
    """Четырехуровневая система памяти"""
    
    def __init__(self, base_path: str = "memory"):
        self.base_path = base_path
        self.levels = {
            "level1_context": MemoryLevel("context", os.path.join(base_path, "level1_context")),
            "level2_dialogs": MemoryLevel("dialogs", os.path.join(base_path, "level2_dialogs")),
            "level3_architecture": MemoryLevel("architecture", os.path.join(base_path, "level3_architecture")),
            "level4_progress": MemoryLevel("progress", os.path.join(base_path, "level4_progress"))
        }
    
    def update_all_levels(self, task: str, data: Dict[str, Any] = None):
        """Обновляет все уровни памяти"""
        timestamp = datetime.now().isoformat()
        
        # Уровень 1: Контекст
        context_data = {
            "current_task": task,
            "timestamp": timestamp,
            "system_status": "active",
            "memory_levels": list(self.levels.keys())
        }
        self.levels["level1_context"].update(context_data)
        
        # Уровень 2: Диалоги
        dialog_data = {
            "timestamp": timestamp,
            "task": task,
            "type": "ai_action",
            "content": f"Обновление памяти: {task}"
        }
        dialogs = self.levels["level2_dialogs"].data.get("dialogs", [])
        dialogs.append(dialog_data)
        self.levels["level2_dialogs"].update({"dialogs": dialogs})
        
        # Уровень 3: Архитектура
        arch_data = {
            "timestamp": timestamp,
            "component": "memory_system",
            "status": "updated",
            "task": task
        }
        architecture = self.levels["level3_architecture"].data.get("components", {})
        architecture["memory_system"] = arch_data
        self.levels["level3_architecture"].update({"components": architecture})
        
        # Уровень 4: Прогресс
        progress_data = {
            "timestamp": timestamp,
            "task": task,
            "status": "completed",
            "phase": "memory_update"
        }
        progress = self.levels["level4_progress"].data.get("tasks", {})
        progress[f"task_{len(progress)}"] = progress_data
        self.levels["level4_progress"].update({"tasks": progress})
        
        return {
            "task": task,
            "timestamp": timestamp,
            "levels_updated": list(self.levels.keys())
        }
    
    def get_summary(self):
        """Получает сводку памяти"""
        summary = {}
        for name, level in self.levels.items():
            level.load()  # Загружаем актуальные данные
            summary[name] = {
                "data_count": len(level.data),
                "last_update": level.data.get("timestamp", "unknown")
            }
        return summary

class CREATORCore:
    """Ядро системы CREATOR"""
    
    def __init__(self):
        self.memory = FourLevelMemory()
        self.session_id = datetime.now().isoformat()
        self.current_task = ""
        
        # Инициализируем память
        self._initialize_memory()
    
    def _initialize_memory(self):
        """Инициализирует систему памяти"""
        init_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "status": "initialized",
            "components": ["memory_system", "core_system"]
        }
        
        self.memory.update_all_levels("Инициализация системы CREATOR", init_data)
        print("✅ Система CREATOR инициализирована")
    
    def execute_task(self, task: str, data: Dict[str, Any] = None):
        """Выполняет задачу с обновлением памяти"""
        self.current_task = task
        
        print(f"🚀 Выполняю задачу: {task}")
        
        # Обновляем память
        result = self.memory.update_all_levels(task, data)
        
        print(f"✅ Задача '{task}' выполнена")
        return result
    
    def get_status(self):
        """Получает статус системы"""
        summary = self.memory.get_summary()
        return {
            "system": "CREATOR Core",
            "session_id": self.session_id,
            "current_task": self.current_task,
            "memory_summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_memory_system(self):
        """Тестирует систему памяти"""
        print("🧪 Тестирование системы памяти...")
        
        # Тестируем обновление памяти
        test_result = self.execute_task("Тестирование памяти", {
            "test_type": "memory_update",
            "status": "success"
        })
        
        # Проверяем статус
        status = self.get_status()
        
        print("✅ Тестирование завершено")
        return {
            "test_result": test_result,
            "status": status
        }

def main():
    """Главная функция"""
    print("🎯 Ядро системы CREATOR - Портал для гуманитариев")
    print("=" * 50)
    
    # Создаем ядро
    core = CREATORCore()
    
    # Тестируем систему
    test_result = core.test_memory_system()
    
    # Выводим статус
    status = core.get_status()
    print("\n📊 Статус системы:")
    print(f"🆔 Session ID: {status['session_id']}")
    print(f"📋 Текущая задача: {status['current_task']}")
    print(f"🧠 Уровней памяти: {len(status['memory_summary'])}")
    
    print("\n🎉 Ядро системы готово к работе!")
    return status

if __name__ == "__main__":
    main()