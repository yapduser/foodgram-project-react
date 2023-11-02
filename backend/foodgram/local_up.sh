#!/bin/bash

ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=1111

# Выполнить миграции
python manage.py migrate

# Создать суперпользователя
echo "from django.contrib.auth import get_user_model; User = get_user_model();
User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')" | python manage.py shell

# Создать теги
add_tag() {
    name="$1"
    color="$2"
    slug="$3"

    echo "from recipes.models import Tag;
Tag.objects.create(name='$name', color='$color', slug='$slug')" | python manage.py shell
}
add_tag "Завтрак" "#FF0000" "breakfast"
add_tag "Обед" "#00FF00" "lunch"
add_tag "Ужин" "#0000FF" "dinner"

# Запустить ингредиент
python manage.py load_data_csv

# Запустить сервер
python manage.py runserver
