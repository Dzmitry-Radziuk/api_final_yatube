# api_final_yatube

Это проект для создания API социальной сети,
использующей Django и Django REST Framework (DRF).
Пользователи могут создавать посты, оставлять комментарии,
подписываться на других пользователей и взаимодействовать с группами.

## Требования

- Python 3.9+
- Django 3.x+
- Django REST Framework
- DRF-YASG (для автогенерации документации)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Dzmitry-Radziuk/api_final_yatube.git

Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate  # Для Windows

Установите зависимости:

pip install -r requirements.txt

Перейдите в директорию проекта:

cd yatube_api

Выполните миграции:

python manage.py migrate

Создайте суперпользователя:

python manage.py createsuperuser
Запустите сервер:

python manage.py runserver
Откройте в браузере http://127.0.0.1:8000/ для доступа к API.

Структура проекта
api/ - основной каталог для обработки запросов:
serializers.py - сериализаторы для моделей.
views.py - вьюсеты и обработчики запросов.
permissions.py - кастомные разрешения.
paginations.py - кастомная пагинация.
urls.py - маршруты API.
posts/ - каталог для моделей и обработки связанных с постами данных:
models.py - модели для постов, комментариев и подписок.
tests/ - тесты для проекта.
API
Пользователи
POST /auth/signup/ - Регистрация нового пользователя.
POST /auth/token/ - Получение токена авторизации.
Посты
GET /posts/ - Получение списка всех постов.
POST /posts/ - Создание нового поста.
GET /posts/{post_id}/ - Получение конкретного поста.
PATCH /posts/{post_id}/ - Редактирование поста.
DELETE /posts/{post_id}/ - Удаление поста.
Комментарии
GET /posts/{post_id}/comments/ - Получение комментариев к посту.
POST /posts/{post_id}/comments/ - Добавление нового комментария к посту.
Подписки
GET /follows/ - Получение списка подписок.
POST /follows/ - Подписка на пользователя.
Группы
GET /groups/ - Получение списка всех групп.
Документация API
Документация доступна по адресу:
http://127.0.0.1:8000/redoc/
Тестирование
Для запуска тестов используйте команду:

pytest
Лицензия
Этот проект находится под лицензией MIT.

Если тебе нужно что-то дополнить или изменить в README, сообщи!
