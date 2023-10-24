from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.constants import LENGTH
from recipes.validators import username_validator, color_validator


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name="email",
        max_length=LENGTH.l_254,
        unique=True,
    )
    username = models.CharField(
        verbose_name="username",
        max_length=LENGTH.l_150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=LENGTH.l_150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=LENGTH.l_150,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="following",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["author"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_user_author",
            )
        ]

    def __str__(self):
        return f"{self.user} подписчик автора - {self.author}"


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        verbose_name="Название",
        max_length=LENGTH.l_200,
        unique=True,
        db_index=True,
    )
    color = models.CharField(
        verbose_name="Цвет",
        max_length=LENGTH.l_7,
        unique=True,
        validators=[color_validator],
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        max_length=LENGTH.l_200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name="Название",
        max_length=LENGTH.l_200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=LENGTH.l_200,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    ...
