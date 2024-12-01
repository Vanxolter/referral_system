referral_system
========


About
-----


Author: Maksim Laurou <Lavrov.python@gmail.com>

Source link: https://github.com/Vanxolter/referral_system

------------------

**ЗАПУСК ПРОЕКТА**

1) Клонируем репозиторий: ``` git clone git@github.com:Vanxolter/referral_system.git ```

2) Создаем виртуальное окружение: ``` virtualenv -p python3 --prompt=rms- venv/ ```

3) Устанавливаем необходимые библиотеки: ``` pip install -r requirements.txt ```

4) Создаем базу данных:
	*  ``` sudo su postgres ```
	* ``` psql ```
	* ``` CREATE USER referral_system WITH PASSWORD 'referral_system' CREATEDB; ```
	* ``` CREATE DATABASE referral_system OWNER referral_system; ```
	* ``` GRANT ALL PRIVILEGES ON DATABASE referral_system TO referral_system; ```

5) Поднимаем миграции: ``` python manage.py migrate ```<br/> 
                       ``` python manage.py makemigrations ```<br/> 
                       ``` python manage.py migrate ```


------------------

**ЗАПУСК DEV КОНТЕЙНЕРА**

1) Сборка билда``` sudo docker compose -f docker-compose.dev.yml build ```
2) Запуск контейнера ``` docker compose -f docker-compose.dev.yml up ```
3) Вход в консоль контейнера ``` docker exec -it django sh ```


------------------

**Нагрузочный тест**
1) ``` wrk -c100 -t4 -d15s http://localhost/ ```
