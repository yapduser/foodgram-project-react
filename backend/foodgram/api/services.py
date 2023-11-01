import base64

from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Ingredient, RecipeIngredient, Recipe, Favorite


class Base64ImageField(serializers.ImageField):
    """Декодирование изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


def add_ingredients(ingredients, recipe):
    """Добавить ингредиенты."""
    ingredient_list = [
        RecipeIngredient(
            recipe=recipe,
            ingredient=Ingredient.objects.get(id=ingredient.get("id")),
            amount=ingredient.get("amount"),
        )
        for ingredient in ingredients
    ]
    RecipeIngredient.objects.bulk_create(ingredient_list)


class RecipeProcessor:
    """Добавить/Удалить рецепт."""

    # def __int__(self, serializer_name):

    @staticmethod
    def __add_recipe(request, instance, serializer_name):
        """Добавить рецепт."""
        serializer = serializer_name(
            data={"user": request.user.id, "recipe": instance.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def __delete_recipe(request, model, instance, error_msg):
        """Удалить рецепт."""
        if not model.objects.filter(
            user=request.user, recipe=instance
        ).exists():
            return Response(
                {"errors": error_msg}, status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.filter(user=request.user, recipe=instance).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_request_method(
        self, request, pk, serializer_name, model_name, err_msg
    ):
        """Проверить тип и обработать запрос."""
        if request.method == "POST":
            try:
                recipe = Recipe.objects.get(id=pk)
            except Recipe.DoesNotExist:
                raise ValidationError(
                    "Рецепт с указанным идентификатором не существует."
                )
            return self.__add_recipe(request, recipe, serializer_name)

        if request.method == "DELETE":
            recipe = get_object_or_404(Recipe, id=pk)
            return self.__delete_recipe(request, model_name, recipe, err_msg)
