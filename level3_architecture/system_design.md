# Архитектура системы CREATOR

## Общая структура

### 1. Четырехуровневая система памяти
```
memory/
├── level1_context/     # Текущий контекст
├── level2_dialogs/     # Диалоги и решения
├── level3_architecture/ # Архитектура системы
└── level4_progress/    # Прогресс разработки
```

### 2. Агентская система
```
agents/
├── langgraph/          # LangGraph агенты
├── letto/             # Letto интеграция
├── memory_manager/     # Управление памятью
└── task_executor/      # Выполнение задач
```

## Компоненты системы

### Backend (Python/FastAPI)
- **API Gateway**: Маршрутизация запросов
- **User Service**: Управление пользователями
- **AI Service**: Интеграция с ИИ-сервисами
- **Memory Service**: Управление памятью
- **Task Service**: Управление задачами

### Frontend (React/TypeScript)
- **Dashboard**: Панель управления
- **User Interface**: Интерфейс для гуманитариев
- **AI Chat**: Чат с ИИ
- **Analytics**: Аналитика и отчеты

### Database (PostgreSQL)
- **Users**: Пользователи и роли
- **Projects**: Проекты и задачи
- **AI_Sessions**: Сессии с ИИ
- **Memory**: Долгосрочная память

### AI Integration
- **OpenAI**: GPT-4, DALL-E
- **Anthropic**: Claude
- **Vector DB**: Chroma/Pinecone
- **RAG**: Retrieval-Augmented Generation

## Микросервисы

### 1. Memory Service
- Управление четырехуровневой памятью
- Синхронизация между уровнями
- Долгосрочное хранение

### 2. Agent Service
- LangGraph агенты
- Letto интеграция
- Автоматизация задач

### 3. AI Service
- Интеграция с ИИ-провайдерами
- Обработка запросов
- Кэширование ответов

### 4. User Service
- Аутентификация
- Управление профилями
- Роли и права

## Инфраструктура (Hetzner)

### Серверы
- **Web Server**: Nginx + React
- **API Server**: FastAPI + Python
- **Database Server**: PostgreSQL
- **AI Server**: GPU для ИИ-моделей

### Мониторинг
- **Prometheus**: Метрики
- **Grafana**: Дашборды
- **ELK Stack**: Логи

## Безопасность
- **SSL/TLS**: Шифрование
- **JWT**: Токены аутентификации
- **Rate Limiting**: Ограничение запросов
- **Input Validation**: Валидация данных