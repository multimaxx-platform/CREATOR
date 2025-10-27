# CREATOR - Портал для гуманитариев с ИИ

## 🎯 Описание проекта

CREATOR - это многопользовательский портал, разработанный для помощи гуманитариям в различных сферах жизни с использованием искусственного интеллекта.

## 🏗️ Архитектура

### Четырехуровневая система памяти
- **Уровень 1**: Контекст - текущее состояние системы
- **Уровень 2**: Диалоги - полные диалоги и решения
- **Уровень 3**: Архитектура - структура системы
- **Уровень 4**: Прогресс - этапы разработки

### Технологический стек
- **Backend**: Python/FastAPI
- **Frontend**: React/TypeScript
- **Database**: PostgreSQL
- **AI Integration**: OpenAI, Anthropic Claude
- **Infrastructure**: Hetzner серверы
- **Memory**: LangGraph + Letto

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск системы
```bash
python main.py
```

### Подключение к Mac M4
```bash
ssh -i ~/.ssh/oleg_key_rsa olegroslavitskiy@195.158.67.204
```

## 📁 Структура проекта

```
CREATOR/
├── agents/                    # Агентская система
│   ├── langgraph/            # LangGraph агенты
│   ├── letto/               # Letto интеграция
│   └── coordinator.py        # Главный координатор
├── memory/                   # Четырехуровневая память
│   ├── level1_context/      # Контекст
│   ├── level2_dialogs/      # Диалоги
│   ├── level3_architecture/ # Архитектура
│   └── level4_progress/     # Прогресс
├── main.py                   # Главный файл запуска
├── requirements.txt          # Зависимости
└── README.md                # Документация
```

## 🤖 Агентская система

### Memory Agent (LangGraph)
- Управляет четырехуровневой памятью
- Автоматическое обновление контекста
- Связи между уровнями памяти

### Letto Integration
- Долгосрочное хранение
- Векторные базы данных
- Семантический поиск

### Coordinator
- Главный координатор системы
- Управление всеми агентами
- Интеграция с Mac M4

## 🔧 Конфигурация

### Переменные окружения
```bash
# Mac M4 подключение
MAC_IP=195.158.67.204
MAC_USER=olegroslavitskiy
SSH_KEY_PATH=~/.ssh/oleg_key_rsa

# AI API ключи
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Letto API
LETTO_API_KEY=your_letto_key
```

## 📊 Мониторинг

### Статус системы
```python
from agents.coordinator import coordinator

status = coordinator.get_project_status()
print(status)
```

### Поиск в памяти
```python
results = coordinator.search_memory("архитектура", level="level3")
print(results)
```

## 🧪 Тестирование

### Запуск тестов
```bash
pytest tests/
```

### Тестирование агентов
```bash
python agents/langgraph/memory_agent.py
python agents/letto/letto_integration.py
python agents/coordinator.py
```

## 🚀 Деплой

### Hetzner серверы
- **Web Server**: Nginx + React
- **API Server**: FastAPI + Python
- **Database Server**: PostgreSQL
- **AI Server**: GPU для ИИ-моделей

### CI/CD
- Автоматический деплой
- Мониторинг и логирование
- Безопасность и SSL

## 📈 Roadmap

### Этап 1: Инициализация ✅
- [x] Создание четырехуровневой памяти
- [x] Подключение LangGraph
- [x] Интеграция Letto

### Этап 2: Архитектура 🔄
- [ ] Детальное проектирование
- [ ] Выбор технологий
- [ ] Создание прототипа

### Этап 3: Backend разработка
- [ ] FastAPI настройка
- [ ] Микросервисы
- [ ] База данных

### Этап 4: Frontend разработка
- [ ] React приложение
- [ ] UI для гуманитариев
- [ ] Интеграция с backend

### Этап 5: ИИ интеграция
- [ ] OpenAI API
- [ ] Anthropic Claude
- [ ] RAG система

### Этап 6: Тестирование
- [ ] Unit тесты
- [ ] Integration тесты
- [ ] E2E тесты

### Этап 7: Деплой
- [ ] Hetzner настройка
- [ ] CI/CD пайплайны
- [ ] Мониторинг

### Этап 8: Запуск
- [ ] Бета-тестирование
- [ ] Исправление багов
- [ ] Публичный запуск

## 👥 Команда

- **Олег Рославицкий** - Директор Multimaxx
- **AI Assistant** - Разработка и архитектура

## 📞 Контакты

- **Компания**: Multimaxx (Мальта)
- **Email**: oleg@multimaxx.com
- **Проект**: CREATOR Portal

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.

---

**Статус**: В разработке  
**Версия**: 1.0.0  
**Последнее обновление**: 2024
