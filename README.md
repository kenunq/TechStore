<h1 align="center"><p>TechStore</p></h1>

<br/>

![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![Django Version](https://img.shields.io/badge/Django-5.0.2-blue)
![DRF Version](https://img.shields.io/badge/DRF-3.14-blue)
![Code Style](https://img.shields.io/badge/code_style-pep8-orange)
___



## Запуск проекта на локальном компьютере

**1. Скачайте проект на локальный компьютер**
```
git clone https://github.com/kenunq/TechStore.git
```

**2. Создайте виртуальное окружение**
```
python -m venv venv
```

**3. Активируйте виртуальное окружение**

*macOS*
```
. venv/bin/activate
```

*linux*
```
source venv/bin/activate
```

*windows*
```
venv\Scripts\activate
```

**4. Обновите пакетный установщик pip**
```
python -m pip install --upgrade pip
```

**5. Зайдите в рабочую директорию проекта(все дальнейшие действия будут осуществляется в ней)**
```
cd TechStore/
```

**6. Установите зависимости необходимые для запуска проекта**
```
pip install -r requirements.txt
```

**7. Сгенерируйте статические файлы**
```
python manage.py collectstatic
```

**8. Создайте файлы миграций**
```
python manage.py makemigrations
```

**9. Примините миграции**
```
python manage.py migrate
```

**10. Создайте файл `.env` и заполните его по примеру**
```
SECRET_KEY = 'secret-key'

EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'email-password-IMAP'
```

**11.Запустите сервер**
```
python manage.py runserver
```


**12. Откройте проект в браузере по адресу**
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

**Для остановки сервера нажмите `CTRL+C` или `CMD+C`(для mac)**

___

## Запуск проекта на локальном компьютере через [Docker](https://www.docker.com/get-started/)

**1. Скачайте проект на локальный компьютер**
```
git clone https://github.com/kenunq/TechStore.git
```

**2. Зайдите в рабочую директорию проекта(все дальнейшие действия будут осуществляется в ней)**
```
cd TechStore/
```

**3. Создайте файл `.env` и заполните его по примеру**
```
SECRET_KEY = 'secret-key'

EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'email-password-IMAP'
```

**4. Запустите Docker Desktop на пк.**

**5. Создайте образ и запустите контейнер**
```
docker compose up --build
```

**6. Откройте проект в браузере по адресу**
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

**Для остановки контейнера нажмите `CTRL+C` или `CMD+C`(для mac) в консоли**