#!/usr/bin/env python3
"""
Скрипт для создания папки на рабочем столе Mac
"""

import os
import subprocess
from pathlib import Path

def create_desktop_folder():
    """Создание папки на рабочем столе"""
    
    # Путь к рабочему столу на Mac
    desktop_path = Path.home() / "Desktop"
    folder_name = "28_июля_тест_Курсор"
    folder_path = desktop_path / folder_name
    
    print(f"🖥️ Рабочий стол: {desktop_path}")
    print(f"📁 Создаю папку: {folder_name}")
    
    try:
        # Создаем папку
        folder_path.mkdir(exist_ok=True)
        print(f"✅ Папка создана: {folder_path}")
        
        # Проверяем создание
        if folder_path.exists():
            print("✅ Папка существует!")
            
            # Создаем тестовый файл внутри
            test_file = folder_path / "test.txt"
            with open(test_file, 'w') as f:
                f.write("Тест от Курсора AI\nСоздано: 28 июля 2024")
            
            print(f"📄 Создан тестовый файл: {test_file}")
            
            # Показываем содержимое рабочего стола
            print("\n📋 Содержимое рабочего стола:")
            for item in desktop_path.iterdir():
                if item.is_dir():
                    print(f"📁 {item.name}")
                else:
                    print(f"📄 {item.name}")
                    
        else:
            print("❌ Ошибка: папка не создана")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def check_system_info():
    """Проверка информации о системе"""
    print("\n🔍 Информация о системе:")
    
    try:
        # Проверяем операционную систему
        import platform
        print(f"OS: {platform.system()} {platform.release()}")
        
        # Проверяем домашнюю директорию
        home = Path.home()
        print(f"Home: {home}")
        
        # Проверяем рабочую директорию
        cwd = Path.cwd()
        print(f"Current: {cwd}")
        
        # Проверяем права доступа
        desktop = home / "Desktop"
        if desktop.exists():
            print(f"Desktop доступен: {desktop}")
            print(f"Права на запись: {os.access(desktop, os.W_OK)}")
        else:
            print("Desktop не найден")
            
    except Exception as e:
        print(f"Ошибка получения информации: {e}")

if __name__ == "__main__":
    print("🚀 Создание папки на рабочем столе")
    print("=" * 40)
    
    check_system_info()
    create_desktop_folder()
    
    print("\n✅ Готово!")