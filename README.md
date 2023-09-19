## Тестовое задание 'Платформа для проверки исходного кода'
Данный проект предоставляет автоматизированную систему для проверки исходного кода загруженных файлов.
Также в нем представлен API-уровень для облегчения работы партнерских компаний.
Для управления очередью используются Celery, Redis и Celery Beat для выполнения периодических задач.


### Стек технологий использованный в проекте:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=ffffff&color=043A6B)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)

### Реализованный Функционал
- Регистрация и аутентификация пользователей с использованием электронной почты и пароля.
- После регистрации пользователи получают письмо для подтверждения своего адреса электронной почты.
- Система загрузки файлов с валидацией, ведением журнала и дальнейшей запланированной проверкой.
- Запланированное информирование клиента о результатах проверки посредством электронной почты.
- Интерфейс списка файлов/файла с информацией о состоянии, результатах отправки отчета, редактирования/удаления файлов.
- Написаны юнит-тесты для основного функционала.
- Были рассмотрены другие методы создания периодических задач и реализован один из них.

### Ресурсы API
- Получение списка файлов пользователя: GET: /api/files/
- Доступ к деталям конкретного файла: GET: /api/files/{file_id}/
- Запрос на повторную проверку конкретного файла: POST: /api/files/{file_id}/




### Запуск на локальном компьютере

Установите Docker [ссылка]('https://www.docker.com'):

Клонируйте репозиторий:
```
git clone git@github.com:askwlc/skypro_checking_projects.git
```

Установите переменные окружения:

Поместите все пароли, токены доступа и другие секреты в файл .env в корне каталога проекта.
Обратитесь к .env.sample для всех необходимых переменных.

Постройте и запустите сервисы:

```
docker-compose up --build -d
```

После успешной сборки выполнить миграции:

```
sudo docker compose exec backend python manage.py migrate
```


Доступ к веб-интерфейсу:

Откройте браузер и перейдите по адресу http://localhost:8000.

Завершение работы:

```
docker-compose down
```

