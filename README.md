# Продуктовый помощник Foodgram

Данные для доступа:
- https://ifoodgram.sytes.net/recipes
- login - admin@admin.com
- pass - admin

## Описание
«Фудграм» — сайт, на котором пользователи публикуют рецепты, добавляют 
чужие рецепты в избранное и подписываются на публикации других авторов. 
Пользователям сайта также доступен сервис «Список покупок». 
Он позволяет создавать список продуктов, которые нужно купить для приготовления 
выбранных блюд.


## Технологии
- Python
- Docker
- PostgreSQL
- Django REST framework
- Gunicorn
- Nginx
- React


## Запуск проекта локально

Клонировать репозиторий:
```shell
git clone git clone <https or SSH URL>
```

Перейти в каталог проекта:
```shell
cd foodgram-project-react
```

Создать .env:
```shell
touch .env
```

Шаблон содержимого для .env файла:
```shell
# Django settings
DEBUG=False
SECRET_KEY=<django_secret_key>
ALLOWED_HOSTS=127.0.0.1;localhost;

# DB
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db_name>
DB_HOST=db
DB_PORT=5432

# Superuser
ADMIN_USERNAME=<usename>
ADMIN_EMAIL=<example@example.com>
ADMIN_PASSWORD=<password>
```

Развернуть приложение:
```shell
docker compose -f docker-compose.dev.yml up -d
```
В процессе развертывания приложения запускается скрипт `backend/foodgram/up.sh`.
- Собирает статику и копирует в volume.
- Выполняет миграции.
- Создает суперпользователя.
- Создает теги.
- Запускает сервер gunicorn.

Выполнить заполнение базы ингредиентами:
```shell
docker compose exec backend python manage.py load_data_csv
```

После успешного запуска, проект доступен на локальном IP `127.0.0.1:8080`.

## Запуск проекта на удаленном сервере

Инструкция предполагает, что удаленный сервер настроен на работу по SSH. 
На сервере установлен Docker. 
Установлен и настроен nginx в качестве балансировщика нагрузки.

Пример конфигурации балансировщика Nginx:

```nginx configuration
server {
    server_name example.com;
    location / {
    	proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8080;
    }
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
server {
    if ($host = example.com) {
        return 301 https://$host$request_uri;
    }
    listen 80;
    return 404;
    server_name example.com;
}
```

Для развертывания на удаленном сервере необходимо клонировать репозиторий на 
локальную машину. Подготовить и загрузить образы на Docker Hub.

Клонировать репозиторий:
```shell
git clone git clone <https or SSH URL>
```

Перейти в каталог проекта:
```shell
cd foodgram-project-react
```

Создать .env:
```shell
touch .env
```

Шаблон содержимого для .env файла:
```shell
# Django settings
DEBUG=False
SECRET_KEY=<django_secret_key>
ALLOWED_HOSTS=127.0.0.1;localhost;<example.com;xxx.xxx.xxx.xxx>

# DB
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db_name>
DB_HOST=db
DB_PORT=5432

# Docker images
BACKEND_IMAGE=<username>/food_back
FRONTEND_IMAGE=<username>/food_front
GATEWAY_IMAGE=<username>/food_gateway

# Superuser
ADMIN_USERNAME=<usename>
ADMIN_EMAIL=<example@example.com>
ADMIN_PASSWORD=<password>
```

Создать docker images образы:
```shell
sudo docker build -t <username>/food_back backend/foodgram
sudo docker build -t <username>/food_front frontend/
sudo docker build -t <username>/food_gateway gateway/
```

Загрузить образы на Docker Hub:
```shell
sudo docker push <username>/food_back
sudo docker push <username>/food_front
sudo docker push <username>/food_gateway
```

Создать на сервере папку `foodgram` 
```shell
mkdir /home/<user name>/foodgram
```

Перенести на удаленный сервер файлы`.env` и `docker-compose.prod.yml`.
```shell
scp .env docker-compose.prod.yml <user@server-address>:/home/<user name>/foodgram
```

Подключиться к серверу:
```shell
ssh user@server-address
```

Перейти в директорию `foodgram`:
```shell
cd /home/<user name>/foodgram
```

Выполнить сборку приложений:
```shell
sudo docker compose -f docker-compose.prod.yml up -d
```

Выполнить заполнение базы ингредиентами:
```shell
docker compose exec backend python manage.py load_data_csv
```

## GitHub Actions
Для использования автоматизированного развертывания и тестирования нужно 
изменить `.github/workflows/main.yml` под свои параметры и задать Actions secrets
в репозитории.

Actions secrets:
- `secrets.DOCKER_USERNAME`
- `secrets.DOCKER_PASSWORD`
- `secrets.HOST`
- `secrets.USER`
- `secrets.SSH_KEY`
- `secrets.SSH_PASSPHRASE`
- `secrets.TELEGRAM_TO`
- `secrets.TELEGRAM_TOKEN`


## Демонстрационные данные
Папка `._misc` содержит дамп базы и изображения для демонстрационного
наполнения сайта.

Для заполнения данными необходимо скопировать на сервер:
- `push_dump.sh`
- `dump_04-11-2023_02_06_31.sql`
- `media/`

Откорректировать файл `push_dump.sh` указав полный путь к media:
`/home/<user>/foodgram/media/`
```shell
#!/bin/bash

docker cp /home/<user>/foodgram/media/. food-back:/app/media
cat <dump_04-11-2023_02_06_31.sql> | docker exec -i food-db psql -U postgres
```

Выполнить:
```shell
./push_dump.sh
```
Данные для доступа:
- https://ifoodgram.sytes.net/recipes
- login - admin@admin.com
- pass - admin
