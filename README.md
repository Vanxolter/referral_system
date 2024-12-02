# Referral System API

## Описание

API для реферальной системы с возможностью авторизации по номеру телефона, активации инвайт-кодов и получения профиля
пользователя.

## Требования

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL

## Установка

1. Клонируйте репозиторий: ``` git clone git@github.com:Vanxolter/referral_system.git ```

2) Создайте виртуальное окружение: ``` virtualenv -p python3 --prompt=rms- venv/ ```

3) Установите необходимые зависимости: ``` pip install -r requirements.txt ```

4) Создайте базу данных:
    * ``` sudo su postgres ```
    * ``` psql ```
    * ``` CREATE USER referral_system WITH PASSWORD 'referral_system' CREATEDB; ```
    * ``` CREATE DATABASE referral_system OWNER referral_system; ```
    * ``` GRANT ALL PRIVILEGES ON DATABASE referral_system TO referral_system; ```

5) Примените миграции: ``` python manage.py migrate ```

------------------

## ЗАПУСК DEV КОНТЕЙНЕРА

1) Сборка билда``` sudo docker compose -f docker-compose.dev.yml build ```
2) Запуск контейнера ``` docker compose -f docker-compose.dev.yml up ```
3) Вход в консоль контейнера ``` docker exec -it django sh ```

------------------

## Нагрузочный тест

1) ``` wrk -c100 -t4 -d15s http://localhost/ ```

------------------

## Документация API

Документация доступна по адресу:

1) ```http://0.0.0.0/swagger/```
2) ```http://0.0.0.0/redoc/```

## Тестирование API

Используйте Postman для тестирования API. Импортируйте коллекцию Postman из файла postman_collection.json (включите этот
файл в репозиторий).

### Доступные эндпоинты

1) Отправка кода авторизации

    - URL: ```/api/v1/send-code/```</br>
    - Метод: POST</br>
    - Тело запроса:</br>
        - ```phone_number```: строка, номер телефона.
        - Пример ответа:
          ```{"message": "Code sent successfully"}```

2) Подтверждение кода и авторизация

    - URL: ```/api/v1/verify-code/```</br>
    - Метод: POST</br>
    - Тело запроса:</br>
        - ```phone_number```: строка, номер телефона.
        - ```code```: строка, 4-значный код.
    - Пример ответа:
      ```{"message": "Login successful", "tokens": { "refresh": "токен_обновления","access": "токен_доступа"}}```

3) Получение профиля пользователя

    - URL: ```/api/v1/profile/```</br>
    - Метод: GET</br>
    - Заголовки:</br>
        - Authorization: Bearer ```<access_token>```
    - Пример ответа:
      ```{"phone_number": "1234567890", "invite_code": "abc123", "activated_invite_code": null, "referred_users": []}```

4) Активация инвайт-кода

    - URL: ```/api/v1/activate-invite/```</br>
    - Метод: POST</br>
    - Тело запроса:</br>
        - ```invite_code```: строка, 6-значный инвайт-код.
    - Пример ответа:
      ```{"message": "Invite code activated successfully"}```
