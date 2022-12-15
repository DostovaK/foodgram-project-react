![example workflow](https://github.com/DostovaK/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Опиcание проекта:
Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Проект доступен:

```
- http://158.160.19.227
- http://158.160.19.227/admin/
```

## Инструкции по установке локально:

Клонируйте репозиторий:
```git clone git@github.com:DostovaK/foodgram-project-react.git```

Установите и активируйте виртуальное окружение:
- для MacOS
```python3 -m venv venv```
```source venv/bin/activate```
- для Windows
```python -m venv venv```
```source venv/Scripts/activate```

Установите зависимости из файла requirements.txt:
```python -m pip install --upgrade pip```
```pip install -r requirements.txt```

Примените миграции:
```python manage.py migrate```

В папке с файлом manage.py выполните команду:
```python manage.py runserver```

## Инструкции по установке на облаке:
Cоздайте файл .env в директории /infra/ с содержанием:

```
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```


Запустите docker compose:
```docker-compose up -d --build```  

Примените миграции:
```sudo docker-compose exec backend python manage.py migrate```

Загрузите ингредиенты:
```sudo docker-compose exec backend python manage.py load_data```


Соберите статику:
```sudo docker-compose exec backend python manage.py collectstatic --noinput```
