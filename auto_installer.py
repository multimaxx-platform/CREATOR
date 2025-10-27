#!/usr/bin/env python3
"""
Автоматический установщик AI-системы управления
Работает как Devin/Interpreter, но эффективнее
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

class AutoInstaller:
    def __init__(self):
        self.mac_home = os.path.expanduser("~")
        self.creator_path = os.path.join(self.mac_home, "CREATOR")
        self.workspace_path = "/workspace"
        
    def log(self, message: str):
        """Логирование с эмодзи"""
        print(f"🔧 {message}")
    
    def run_command(self, command: list, cwd: str = None) -> dict:
        """Выполнение команды с обработкой ошибок"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=60
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
    
    def check_mac_connection(self) -> bool:
        """Проверка подключения к Mac"""
        self.log("Проверяю подключение к Mac...")
        
        # Проверяем доступ к домашней директории Mac
        if os.path.exists(self.mac_home):
            self.log(f"✅ Mac доступен: {self.mac_home}")
            return True
        else:
            self.log(f"❌ Mac недоступен: {self.mac_home}")
            return False
    
    def copy_files_to_mac(self) -> bool:
        """Копирование файлов на Mac"""
        self.log("Копирую файлы на Mac...")
        
        # Создаем папку CREATOR если не существует
        if not os.path.exists(self.creator_path):
            os.makedirs(self.creator_path, exist_ok=True)
            self.log(f"📁 Создана папка: {self.creator_path}")
        
        # Список файлов для копирования
        files_to_copy = [
            "system_bridge.py",
            "mac_client.py", 
            "ai_system_manager.py",
            "local_ai_assistant.py",
            "requirements_ai_system.txt",
            "INSTALL.md"
        ]
        
        copied_count = 0
        for file_name in files_to_copy:
            source_path = os.path.join(self.workspace_path, file_name)
            dest_path = os.path.join(self.creator_path, file_name)
            
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, dest_path)
                    self.log(f"✅ Скопирован: {file_name}")
                    copied_count += 1
                except Exception as e:
                    self.log(f"❌ Ошибка копирования {file_name}: {e}")
            else:
                self.log(f"⚠️ Файл не найден: {file_name}")
        
        self.log(f"📊 Скопировано файлов: {copied_count}/{len(files_to_copy)}")
        return copied_count > 0
    
    def setup_virtual_environment(self) -> bool:
        """Настройка виртуального окружения на Mac"""
        self.log("Настраиваю виртуальное окружение...")
        
        venv_path = os.path.join(self.creator_path, "gpt_venv")
        
        # Проверяем существование venv
        if os.path.exists(venv_path):
            self.log("✅ Виртуальное окружение уже существует")
            return True
        
        # Создаем новое виртуальное окружение
        self.log("Создаю новое виртуальное окружение...")
        result = self.run_command(["python3", "-m", "venv", venv_path])
        
        if result["success"]:
            self.log("✅ Виртуальное окружение создано")
            return True
        else:
            self.log(f"❌ Ошибка создания venv: {result['error']}")
            return False
    
    def install_dependencies(self) -> bool:
        """Установка зависимостей"""
        self.log("Устанавливаю зависимости...")
        
        venv_pip = os.path.join(self.creator_path, "gpt_venv", "bin", "pip")
        requirements_file = os.path.join(self.creator_path, "requirements_ai_system.txt")
        
        if not os.path.exists(venv_pip):
            self.log("❌ pip не найден в виртуальном окружении")
            return False
        
        # Устанавливаем зависимости
        result = self.run_command([venv_pip, "install", "-r", requirements_file])
        
        if result["success"]:
            self.log("✅ Зависимости установлены")
            return True
        else:
            self.log(f"❌ Ошибка установки зависимостей: {result['error']}")
            return False
    
    def create_startup_script(self) -> bool:
        """Создание скрипта автозапуска"""
        self.log("Создаю скрипт автозапуска...")
        
        startup_script = os.path.join(self.creator_path, "start_ai_system.sh")
        
        script_content = """#!/bin/bash

# AI System Startup Script
echo "🚀 Запуск AI-системы управления..."

# Активируем виртуальное окружение
source ~/CREATOR/gpt_venv/bin/activate

# Запускаем системный мост в фоне
echo "📡 Запуск системного моста..."
python ~/CREATOR/system_bridge.py &
BRIDGE_PID=$!

# Ждем запуска моста
sleep 3

# Запускаем AI-ассистент
echo "🤖 Запуск AI-ассистента..."
python ~/CREATOR/local_ai_assistant.py

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
    
    def create_telegram_integration(self) -> bool:
        """Создание интеграции с Telegram ботом"""
        self.log("Создаю интеграцию с Telegram...")
        
        telegram_integration = os.path.join(self.creator_path, "ai_telegram_bot.py")
        
        integration_code = '''#!/usr/bin/env python3
"""
AI Telegram бот с локальным ассистентом
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from local_ai_assistant import LocalAIAssistant

# Инициализация AI-ассистента
ai_assistant = LocalAIAssistant()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_message = """🤖 AI-ассистент системы готов к работе!

Доступные команды:
• /diagnostic - диагностика системы
• /disk - информация о диске
• /memory - информация о памяти
• /project - анализ проекта
• /help - справка

Или просто напишите запрос на русском языке!"""
    
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех сообщений"""
    user_message = update.message.text
    
    # Отправляем запрос AI-ассистенту
    response = ai_assistant.process_user_request(user_message)
    
    # Отправляем ответ пользователю
    await update.message.reply_text(response["message"])

async def diagnostic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда диагностики"""
    response = ai_assistant.process_user_request("диагностика")
    await update.message.reply_text(response["message"])

async def disk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда информации о диске"""
    response = ai_assistant.process_user_request("диск")
    await update.message.reply_text(response["message"])

async def memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда информации о памяти"""
    response = ai_assistant.process_user_request("память")
    await update.message.reply_text(response["message"])

async def project_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда анализа проекта"""
    response = ai_assistant.process_user_request("проект")
    await update.message.reply_text(response["message"])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда помощи"""
    help_text = ai_assistant.get_help_message()
    await update.message.reply_text(help_text)

def main():
    """Запуск бота"""
    # Ваш токен бота (замените на свой)
    bot_token = "8347085046:AAGPyliO9bXmPqIN97m-3lR-qS9M4_ILfrU"
    
    # Создаем приложение
    application = Application.builder().token(bot_token).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("diagnostic", diagnostic_command))
    application.add_handler(CommandHandler("disk", disk_command))
    application.add_handler(CommandHandler("memory", memory_command))
    application.add_handler(CommandHandler("project", project_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчик всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 AI Telegram бот запущен!")
    print("📱 Отправьте /start в боте для начала работы")
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
'''
        
        try:
            with open(telegram_integration, 'w') as f:
                f.write(integration_code)
            
            os.chmod(telegram_integration, 0o755)
            self.log("✅ Telegram интеграция создана")
            return True
        except Exception as e:
            self.log(f"❌ Ошибка создания Telegram интеграции: {e}")
            return False
    
    def test_system(self) -> bool:
        """Тестирование системы"""
        self.log("Тестирую систему...")
        
        # Проверяем основные файлы
        required_files = [
            "system_bridge.py",
            "mac_client.py",
            "local_ai_assistant.py",
            "ai_telegram_bot.py"
        ]
        
        for file_name in required_files:
            file_path = os.path.join(self.creator_path, file_name)
            if os.path.exists(file_path):
                self.log(f"✅ {file_name} найден")
            else:
                self.log(f"❌ {file_name} не найден")
                return False
        
        self.log("✅ Все файлы на месте")
        return True
    
    def install(self) -> bool:
        """Полная установка системы"""
        self.log("🚀 Начинаю автоматическую установку AI-системы...")
        
        # Проверяем подключение к Mac
        if not self.check_mac_connection():
            return False
        
        # Копируем файлы
        if not self.copy_files_to_mac():
            return False
        
        # Настраиваем виртуальное окружение
        if not self.setup_virtual_environment():
            return False
        
        # Устанавливаем зависимости
        if not self.install_dependencies():
            return False
        
        # Создаем скрипт автозапуска
        if not self.create_startup_script():
            return False
        
        # Создаем Telegram интеграцию
        if not self.create_telegram_integration():
            return False
        
        # Тестируем систему
        if not self.test_system():
            return False
        
        self.log("🎉 Установка завершена успешно!")
        self.log("📋 Следующие шаги:")
        self.log("1. cd ~/CREATOR")
        self.log("2. ./start_ai_system.sh")
        self.log("3. Или запустите: python ai_telegram_bot.py")
        
        return True

def main():
    """Главная функция"""
    installer = AutoInstaller()
    
    print("🤖 Автоматический установщик AI-системы")
    print("=" * 50)
    
    if installer.install():
        print("\n✅ Установка завершена успешно!")
        print("🎯 Ваш Mac теперь управляется AI!")
    else:
        print("\n❌ Установка не удалась")
        print("🔧 Проверьте логи выше")

if __name__ == "__main__":
    main()