#!/bin/bash

# Выполнить миграции
python manage.py migrate

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
