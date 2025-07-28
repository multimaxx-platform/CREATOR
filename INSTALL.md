# 🤖 AI-Системный Менеджер - Инструкция по установке

## 📋 Что это такое?

Система для интеллектуального управления вашим Mac через AI. Состоит из:

- **Системный мост** (`system_bridge.py`) - API сервер с безопасными командами
- **Mac клиент** (`mac_client.py`) - подключение к мосту
- **AI менеджер** (`ai_system_manager.py`) - интеллектуальное управление

## 🚀 Быстрая установка

### 1. Копирование файлов на ваш Mac

```bash
# Скопируйте файлы из /workspace в вашу папку
cp /workspace/system_bridge.py ~/CREATOR/
cp /workspace/mac_client.py ~/CREATOR/
cp /workspace/ai_system_manager.py ~/CREATOR/
```

### 2. Установка зависимостей

```bash
# Активируйте виртуальное окружение
source ~/CREATOR/gpt_venv/bin/activate

# Установите необходимые пакеты
pip install flask requests
```

### 3. Запуск системного моста

```bash
cd ~/CREATOR
python system_bridge.py
```

Вы увидите:
```
🚀 Системный мост запущен!
📡 API доступен на http://localhost:5000
🔒 Только безопасные команды разрешены
```

### 4. Тестирование клиента

В новом терминале:
```bash
cd ~/CREATOR
source ~/CREATOR/gpt_venv/bin/activate
python mac_client.py
```

### 5. Запуск AI-менеджера

```bash
python ai_system_manager.py
```

## 🔧 Настройка безопасности

### Разрешенные команды:
- `system_info` - информация о системе
- `disk_space` - дисковое пространство
- `memory_usage` - использование памяти
- `process_list` - список процессов
- `network_status` - статус сети
- `file_list` - список файлов
- `git_status` - статус Git
- `python_version` - версия Python
- `pip_list` - список пакетов
- `brew_list` - список Homebrew пакетов

### Добавление новых команд:

Отредактируйте `system_bridge.py`:

```python
self.safe_commands = {
    # ... существующие команды ...
    'your_command': ['your', 'command', 'args'],
}
```

## 📊 Возможности системы

### 🔍 Диагностика системы
- Анализ здоровья системы
- Проверка дискового пространства
- Мониторинг памяти
- Анализ процессов

### ⚙️ Оптимизация разработки
- Анализ проектов
- Проверка зависимостей
- Git статус
- Рекомендации по улучшению

### 🛠️ Управление инструментами
- Установка пакетов
- Создание структуры проектов
- Автоматизация задач

### 📁 Управление проектами
- Создание структуры Python проектов
- Создание веб-проектов
- Автоматическая инициализация

## 🔄 Интеграция с Telegram ботом

Добавьте в ваш `gpt_telegram_agent.py`:

```python
from ai_system_manager import AISystemManager

# В обработчике сообщений
manager = AISystemManager()

if "диагностика" in message.lower():
    diagnostic = manager.run_diagnostic()
    await update.message.reply_text(f"Результаты диагностики: {diagnostic}")

if "оптимизация" in message.lower():
    optimization = manager.optimize_development_environment()
    await update.message.reply_text(f"Рекомендации: {optimization}")
```

## 🛡️ Безопасность

### Ограничения:
- ✅ Только безопасные команды
- ✅ Таймаут 30 секунд
- ✅ Логирование всех действий
- ✅ Проверка перед выполнением

### Мониторинг:
- Логи сохраняются в `system_bridge.log`
- Все команды записываются с временными метками
- Ошибки обрабатываются безопасно

## 🚨 Устранение неполадок

### Ошибка подключения:
```bash
# Проверьте, что мост запущен
curl http://localhost:5000/api/system/info
```

### Ошибка зависимостей:
```bash
pip install --upgrade flask requests
```

### Проблемы с правами:
```bash
chmod +x system_bridge.py
chmod +x mac_client.py
chmod +x ai_system_manager.py
```

## 📈 Расширение функциональности

### Добавление новых API endpoints:

В `system_bridge.py`:
```python
@app.route('/api/custom/endpoint', methods=['POST'])
def custom_endpoint():
    # Ваша логика
    return jsonify({"result": "success"})
```

### Интеграция с другими AI:

```python
# Подключение к OpenAI API
import openai
client = openai.OpenAI(api_key="your-key")

# Анализ с помощью GPT
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": system_data}]
)
```

## 🎯 Примеры использования

### Автоматическая диагностика:
```python
manager = AISystemManager()
diagnostic = manager.run_diagnostic()
print("Система готова к работе!" if diagnostic else "Требуется внимание")
```

### Создание проекта:
```python
manager = AISystemManager()
result = manager.create_project_structure("my_awesome_project", "python")
```

### Установка инструментов:
```python
manager = AISystemManager()
tools = ["requests", "flask", "pandas"]
manager.install_development_tools(tools)
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в `system_bridge.log`
2. Убедитесь, что все зависимости установлены
3. Проверьте права доступа к файлам
4. Убедитесь, что порт 5000 свободен

---

**🎉 Поздравляем! Ваш Mac теперь управляется AI!**