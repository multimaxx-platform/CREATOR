#!/usr/bin/env python3
"""
Главный файл запуска системы CREATOR
Четырехуровневая память + LangGraph + Letto
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, Any

# Добавляем пути
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from agents.coordinator import coordinator, mac_integration

class CREATORSystem:
    """Главная система CREATOR"""
    
    def __init__(self):
        self.coordinator = coordinator
        self.mac_integration = mac_integration
        self.start_time = datetime.now()
        
    async def initialize_system(self):
        """Инициализирует систему"""
        print("🚀 Инициализация системы CREATOR...")
        
        # Проверяем статус Mac
        print("📱 Проверяем подключение к Mac M4...")
        mac_status = self.mac_integration.check_creator_status()
        
        if mac_status["success"]:
            print("✅ Подключение к Mac успешно")
            print(f"📋 Статус CREATOR: {mac_status['stdout']}")
        else:
            print("⚠️ Проблема с подключением к Mac")
            print(f"❌ Ошибка: {mac_status.get('error', 'Unknown error')}")
        
        # Инициализируем память
        print("🧠 Инициализация четырехуровневой памяти...")
        init_result = self.coordinator.execute_task("Запуск системы CREATOR")
        
        print("✅ Система CREATOR готова к работе!")
        return init_result
    
    async def run_autonomous_session(self, duration_hours: int = 4):
        """Запускает автономную сессию"""
        print(f"🤖 Запуск автономной сессии на {duration_hours} часов...")
        
        # План работы
        tasks = [
            "Анализ текущего состояния проекта",
            "Создание архитектуры портала",
            "Настройка backend (FastAPI)",
            "Разработка frontend (React)",
            "Интеграция с ИИ-сервисами",
            "Тестирование системы",
            "Подготовка к деплою"
        ]
        
        for i, task in enumerate(tasks, 1):
            print(f"\n📋 Задача {i}/{len(tasks)}: {task}")
            
            # Выполняем задачу
            result = self.coordinator.execute_task(task)
            
            # Логируем прогресс
            self.coordinator.log_progress(f"phase_{i}", {
                "task": task,
                "status": "completed",
                "result": result
            })
            
            print(f"✅ Задача '{task}' выполнена")
            
            # Небольшая пауза между задачами
            await asyncio.sleep(1)
        
        print("\n🎉 Автономная сессия завершена!")
        return self.coordinator.get_project_status()
    
    def get_system_status(self):
        """Получает статус системы"""
        return {
            "system": "CREATOR",
            "start_time": self.start_time.isoformat(),
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "status": "running",
            "project_status": self.coordinator.get_project_status()
        }

async def main():
    """Главная функция"""
    print("🎯 Система CREATOR - Портал для гуманитариев")
    print("=" * 50)
    
    # Создаем систему
    system = CREATORSystem()
    
    # Инициализируем
    await system.initialize_system()
    
    # Запускаем автономную сессию
    result = await system.run_autonomous_session(duration_hours=4)
    
    # Выводим финальный статус
    status = system.get_system_status()
    print("\n📊 Финальный статус системы:")
    print(f"⏱️ Время работы: {status['uptime']:.2f} секунд")
    print(f"📈 Задач выполнено: {len(result.get('summary', {}).get('progress_tasks', []))}")
    
    return status

if __name__ == "__main__":
    # Запускаем систему
    asyncio.run(main())
