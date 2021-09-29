**API_Yatube**
=====

Сервис YaMDb работает на основе  REST API интерфейса. Сервис собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Регистрация пользователей реализована посредством отправки кода подтверждения на e-mail, аутентификация производится по JWT-токену.
Пользователи могут оставлять отзывы и балльные оценки к произведениям, читать и комментировать отзывы других авторов.

**Как запустить проект:**
-----

Клонировать репозиторий и перейти в него в командной строке:

.. code-block:: text

 git clone https://github.com/RWSNTi/api_yamdb.git

Перейти в созданный репозиторий:

.. code-block:: text

 cd api_final_yatube

Cоздать и активировать виртуальное окружение:

.. code-block:: text

 python -m venv venv
 source venv/scripts/activate

Обновить установщик расширений pip

.. code-block:: text

 python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:

.. code-block:: text

 pip install -r requirements.txt
 
Выполнить миграции:

.. code-block:: text

 python manage.py migrate

Запустить проект:

.. code-block:: text

 python manage.py runserver

**Документация с примерами запросов и ответов будет доступна после развёртывания и запуска проекта по ссылке http://127.0.0.1:8000/redoc/**
