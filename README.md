# Habit Tracker

## Описание проекта

Это проект Habit Tracker, который позволяет пользователям создавать, отслеживать и управлять своими привычками. Проект включает в себя интеграцию с Telegram для отправки уведомлений о привычках.

## Установка

1.  Клонируйте репозиторий:
    ```bash
    git clone <your_repository_url>
    ```
2.  Перейдите в директорию проекта:
    ```bash
    cd habit_tracker
    ```
3.  Создайте и активируйте виртуальное окружение Poetry:
    ```bash
    poetry install
    poetry shell
    ```
4.  Установите зависимости:
    ```bash
    poetry install
    ```
5.  Создайте файл `.env` и добавьте необходимые переменные окружения (см. раздел "Настройка переменных окружения").
6.  Выполните миграции:
    ```bash
    python manage.py migrate
    ```
7.  Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```
8.  Запустите сервер:
    ```bash
    python manage.py runserver
    ```
9.  Запустите Celery worker:
    ```bash
    celery -A config worker -l info
    ```

## Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:
*   `SECRET_KEY` - Секретный ключ Django.  Сгенерируйте случайный ключ и вставьте его сюда.  Пример: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
*   `DEBUG` - Режим отладки. `True` для разработки, `False` для production.
*   `DATABASE_URL` - URL для подключения к базе данных PostgreSQL. Пример: `postgres://user:password@localhost:5432/habit_tracker_db`. Замените `<user>`, `<password>`, `<host>`, `<port>` и `<database>` на ваши значения.
*   `REDIS_URL` - URL для подключения к Redis.  Пример: `redis://localhost:6379/0`.  Если Redis требует пароль, добавьте его в URL, например: `redis://:password@localhost:6379/0`.
*   `TELEGRAM_BOT_TOKEN` - Токен вашего Telegram бота. Укажите токен, полученный от BotFather.
*	`ALLOWED_HOSTS` - Список разрешенных хостов. В production укажите домены, с которых будет доступен ваш сайт.

## Запуск тестов

pytest

## Документация API
Документация API доступна по адресу: /swagger/ или /redoc/ после запуска сервера.

## Интеграция с Telegram
Для работы с Telegram необходимо создать бота и получить его токен. Затем необходимо настроить переменные окружения и запустить Celery worker.

## Зависимости
Django
Django REST Framework
djangorestframework-simplejwt
django-cors-headers
psycopg2-binary
celery
redis
python-dotenv
drf-yasg
pytest
pytest-django
flake8
requests