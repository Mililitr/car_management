# Car Management System

## Описание
Веб-приложение для управления информацией об автомобилях с использованием Django и DRF.

## Функционал
- Регистрация и авторизация пользователей
- CRUD операции с автомобилями
- Система комментариев
- REST API
- Административная панель

## Установка
1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать виртуальное окружение:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Выполнить миграции: `python manage.py migrate`
6. Создать суперпользователя: `python manage.py createsuperuser`
7. Запустить сервер: `python manage.py runserver`

## API Endpoints
- GET /api/cars/ - Список всех автомобилей
- POST /api/cars/ - Создание нового автомобиля
- GET /api/cars/{id}/ - Детали автомобиля
- PUT /api/cars/{id}/ - Обновление автомобиля
- DELETE /api/cars/{id}/ - Удаление автомобиля
- GET /api/cars/{id}/comments/ - Список комментариев
- POST /api/cars/{id}/comments/ - Добавление комментария

## Технологии
- Python
- Django
- DRF
- SQLite