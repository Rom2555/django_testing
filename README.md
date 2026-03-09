# Django Testing Project

## Описание

Учебный Django-проект для демонстрации работы с Django REST Framework и написания тестов. Проект представляет собой систему управления курсами и студентами с REST API.

## Технологический стек

- **Django 3.1** - веб-фреймворк
- **Django REST Framework** - создание REST API
- **django-filter** - фильтрация queryset-ов
- **PostgreSQL** - база данных
- **pytest** - тестовый фреймворк
- **model_bakery** - генерация тестовых данных

## Модели

### Student
- `name` - имя студента (TextField)
- `birth_date` - дата рождения (DateField, опционально)

### Course
- `name` - название курса (TextField)
- `students` - связь ManyToMany со студентами

## API Endpoints

Базовый URL: `/api/v1/`

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/v1/courses/` | Получить список курсов |
| POST | `/api/v1/courses/` | Создать новый курс |
| GET | `/api/v1/courses/{id}/` | Получить курс по ID |
| PUT | `/api/v1/courses/{id}/` | Обновить курс |
| DELETE | `/api/v1/courses/{id}/` | Удалить курс |

## Параметры фильтрации

Для списка курсов доступны следующие фильтры:

- `id` - фильтр по ID курса
- `name` - фильтр по названию курса

Примеры запросов:
```
GET /api/v1/courses/?name=Python
GET /api/v1/courses/?id=1
```

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements-dev.txt
```

2. Настройте базу данных в `django_testing/settings.py`

3. Выполните миграции:
```bash
python manage.py migrate
```

4. Запустите сервер:
```bash
python manage.py runserver
```

## Тестирование

Запуск всех тестов:
```bash
pytest
```
## Тестовые фикстуры

В `tests/conftest.py` определены следующие фикстуры:

- `api_client` - тестовый API-клиент DRF
- `course_factory` - фабрика для создания курсов
- `student_factory` - фабрика для создания студентов

## Примеры использования API

### Создание курса
```bash
curl -X POST http://localhost:8000/api/v1/courses/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Python"}'
```

### Получение списка курсов
```bash
curl http://localhost:8000/api/v1/courses/
```

### Фильтрация по названию
```bash
curl "http://localhost:8000/api/v1/courses/?name=Python"
```

## Особенности реализации

- URL-маршруты генерируются автоматически с помощью `DefaultRouter`
- Для построения URL в тестах используется функция `reverse()`
- Фильтрация реализована через `django_filters`
- Тесты используют паттерн фабрик через `model_bakery`
