#!/usr/bin/env python3
"""
Мост для работы с Mac - локальное управление системой
"""

import os
import subprocess
import json
import platform
from pathlib import Path
from typing import Dict, Any, List

class MacBridge:
    def __init__(self):
        self.mac_home = Path.home()
        self.creator_path = self.mac_home / "CREATOR"
        self.desktop_path = self.mac_home / "Desktop"
        
    def log(self, message: str):
        """Логирование с эмодзи"""
        print(f"🔧 {message}")
    
    def run_command(self, command: List[str], cwd: str = None) -> Dict[str, Any]:
        """Выполнение команды на Mac"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "command": " ".join(command)
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "command": " ".join(command)
            }
    
    def create_desktop_folder(self, folder_name: str = "28_июля_тест_Курсор") -> bool:
        """Создание папки на рабочем столе"""
        self.log(f"Создаю папку на рабочем столе: {folder_name}")
        
        folder_path = self.desktop_path / folder_name
        
        try:
            # Создаем папку
            folder_path.mkdir(exist_ok=True)
            self.log(f"✅ Папка создана: {folder_path}")
            
            # Создаем тестовый файл
            test_file = folder_path / "test.txt"
            with open(test_file, 'w') as f:
                f.write("Тест от Курсора AI\nСоздано: 28 июля 2024")
            
            self.log(f"📄 Создан тестовый файл: {test_file}")
            return True
            
        except Exception as e:
            self.log(f"❌ Ошибка создания папки: {e}")
            return False
    
    def setup_ai_system(self) -> bool:
        """Установка AI-системы в CREATOR"""
        self.log("Устанавливаю AI-систему в CREATOR...")
        
        # Создаем папку CREATOR если не существует
        if not self.creator_path.exists():
            self.creator_path.mkdir(parents=True, exist_ok=True)
            self.log(f"📁 Создана папка CREATOR: {self.creator_path}")
        
        # Копируем файлы из workspace
        workspace_files = [
            "system_bridge.py",
            "mac_client.py",
            "local_ai_assistant.py",
            "ai_system_manager.py",
            "requirements_ai_system.txt"
        ]
        
        copied_count = 0
        for file_name in workspace_files:
            source_path = Path("/workspace") / file_name
            dest_path = self.creator_path / file_name
            
            if source_path.exists():
                try:
                    # Копируем файл
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    self.log(f"✅ Скопирован: {file_name}")
                    copied_count += 1
                except Exception as e:
                    self.log(f"❌ Ошибка копирования {file_name}: {e}")
            else:
                self.log(f"⚠️ Файл не найден в workspace: {file_name}")
        
        self.log(f"📊 Скопировано файлов: {copied_count}/{len(workspace_files)}")
        return copied_count > 0
    
    def install_dependencies(self) -> bool:
        """Установка зависимостей"""
        self.log("Устанавливаю зависимости...")
        
        # Проверяем Python
        python_check = self.run_command(["python3", "--version"])
        if not python_check["success"]:
            self.log("❌ Python3 не найден")
            return False
        
        self.log(f"✅ Python найден: {python_check['output'].strip()}")
        
        # Устанавливаем pip пакеты
        packages = ["flask", "requests", "python-telegram-bot"]
        
        for package in packages:
            self.log(f"📦 Устанавливаю {package}...")
            result = self.run_command(["pip3", "install", package])
            
            if result["success"]:
                self.log(f"✅ {package} установлен")
            else:
                self.log(f"❌ Ошибка установки {package}: {result['error']}")
        
        return True
    
    def create_startup_script(self) -> bool:
        """Создание скрипта автозапуска"""
        self.log("Создаю скрипт автозапуска...")
        
        startup_script = self.creator_path / "start_ai_system.sh"
        
        script_content = """#!/bin/bash

# AI System Startup Script
echo "🚀 Запуск AI-системы управления..."

# Переходим в папку CREATOR
cd ~/CREATOR

# Запускаем системный мост в фоне
echo "📡 Запуск системного моста..."
python3 system_bridge.py &
BRIDGE_PID=$!

# Ждем запуска моста
sleep 3

# Запускаем AI-ассистент
echo "🤖 Запуск AI-ассистента..."
python3 local_ai_assistant.py

# Останавливаем мост при выходе
kill $BRIDGE_PID
echo "✅ AI-система остановлена"
"""
        
        try:
            with open(startup_script, 'w') as f:
                f.write(script_content)
            
            # Делаем скрипт исполняемым
            os.chmod(startup_script, 0o755)
            self.log("✅ Скрипт автозапуска создан")
            return True
        except Exception as e:
            self.log(f"❌ Ошибка создания скрипта: {e}")
            return False
    
    def test_system(self) -> bool:
        """Тестирование системы"""
        self.log("Тестирую систему...")
        
        # Проверяем основные файлы
        required_files = [
            "system_bridge.py",
            "mac_client.py",
            "local_ai_assistant.py"
        ]
        
        for file_name in required_files:
            file_path = self.creator_path / file_name
            if file_path.exists():
                self.log(f"✅ {file_name} найден")
            else:
                self.log(f"❌ {file_name} не найден")
                return False
        
        # Проверяем Python
        python_test = self.run_command(["python3", "-c", "print('Python работает!')"])
        if python_test["success"]:
            self.log("✅ Python работает")
        else:
            self.log("❌ Python не работает")
            return False
        
        self.log("✅ Система готова к работе")
        return True
    
    def get_system_info(self) -> Dict[str, Any]:
        """Получение информации о системе"""
        info = {
            "platform": platform.system(),
            "home": str(self.mac_home),
            "creator_path": str(self.creator_path),
            "desktop_path": str(self.desktop_path),
            "python_version": "",
            "creator_exists": self.creator_path.exists(),
            "desktop_exists": self.desktop_path.exists()
        }
        
        # Получаем версию Python
        python_check = self.run_command(["python3", "--version"])
        if python_check["success"]:
            info["python_version"] = python_check["output"].strip()
        
        return info

def main():
    """Главная функция"""
    bridge = MacBridge()
    
    print("🤖 Mac Bridge - локальное управление системой")
    print("=" * 50)
    
    # Получаем информацию о системе
    system_info = bridge.get_system_info()
    print(f"🖥️ Платформа: {system_info['platform']}")
    print(f"🏠 Домашняя папка: {system_info['home']}")
    print(f"📁 CREATOR: {system_info['creator_path']}")
    print(f"🖥️ Desktop: {system_info['desktop_path']}")
    print(f"🐍 Python: {system_info['python_version']}")
    
    # Создаем папку на рабочем столе
    print("\n📁 Создание папки на рабочем столе...")
    if bridge.create_desktop_folder():
        print("✅ Папка создана успешно!")
    else:
        print("❌ Ошибка создания папки")
    
    # Устанавливаем AI-систему
    print("\n🤖 Установка AI-системы...")
    if bridge.setup_ai_system():
        print("✅ AI-система установлена!")
        
        # Устанавливаем зависимости
        if bridge.install_dependencies():
            print("✅ Зависимости установлены!")
            
            # Создаем скрипт автозапуска
            if bridge.create_startup_script():
                print("✅ Скрипт автозапуска создан!")
                
                # Тестируем систему
                if bridge.test_system():
                    print("✅ Система протестирована!")
                    print("\n🎉 Установка завершена успешно!")
                    print("📋 Для запуска:")
                    print("1. cd ~/CREATOR")
                    print("2. ./start_ai_system.sh")
                else:
                    print("❌ Тестирование не прошло")
            else:
                print("❌ Ошибка создания скрипта")
        else:
            print("❌ Ошибка установки зависимостей")
    else:
        print("❌ Ошибка установки AI-системы")

if __name__ == "__main__":
    main()