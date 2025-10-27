#!/bin/bash

echo "🚀 Копирование файлов AI-системы на ваш Mac..."

# Проверяем, существует ли папка CREATOR
if [ ! -d "$HOME/CREATOR" ]; then
    echo "📁 Создаю папку CREATOR..."
    mkdir -p "$HOME/CREATOR"
fi

# Копируем файлы
echo "📋 Копирую файлы..."

# Основные файлы системы
cp /workspace/system_bridge.py "$HOME/CREATOR/"
cp /workspace/mac_client.py "$HOME/CREATOR/"
cp /workspace/ai_system_manager.py "$HOME/CREATOR/"
cp /workspace/INSTALL.md "$HOME/CREATOR/"
cp /workspace/requirements_ai_system.txt "$HOME/CREATOR/"

# Делаем файлы исполняемыми
chmod +x "$HOME/CREATOR/system_bridge.py"
chmod +x "$HOME/CREATOR/mac_client.py"
chmod +x "$HOME/CREATOR/ai_system_manager.py"

echo "✅ Файлы скопированы в $HOME/CREATOR/"
echo ""
echo "📋 Скопированные файлы:"
ls -la "$HOME/CREATOR/"*.py
echo ""
echo "🚀 Следующие шаги:"
echo "1. cd ~/CREATOR"
echo "2. source ~/CREATOR/gpt_venv/bin/activate"
echo "3. pip install flask requests"
echo "4. python system_bridge.py"
echo ""
echo "🎉 Готово! Теперь можете запускать AI-систему!"