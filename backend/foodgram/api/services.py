import base64

from django.core.files.base import ContentFile
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Ingredient, RecipeIngredient, Recipe


CREATED = status.HTTP_201_CREATED
NO_CONTENT = status.HTTP_204_NO_CONTENT
BAD_REQUEST = status.HTTP_400_BAD_REQUEST


class Base64ImageField(serializers.ImageField):
    """Декодирование изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipeProcessor:
    """Добавить/Удалить рецепт."""

    def __init__(self, serializer_name, model, request, pk, err_msg):
        self.serializer_name = serializer_name
        self.model = model
        self.request = request
        self.method = request.method
        self.user = request.user
        self.pk = pk
        self.err_msg = err_msg

    def __add_recipe(self, recipe):
        """Добавить рецепт."""
        serializer = self.serializer_name(
            data={"user": self.user.id, "recipe": recipe.id},
            context={"request": self.request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=CREATED)

    def __delete_recipe(self, recipe):
        """Удалить рецепт."""
        obj = self.model.objects.filter(user=self.user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=NO_CONTENT)
        return Response({"errors": self.err_msg}, status=BAD_REQUEST)

    def execute(self):
        """Проверить тип и обработать запрос."""
        if self.method == "POST":
            try:
                recipe = Recipe.objects.get(id=self.pk)
            except Recipe.DoesNotExist:
                raise ValidationError(
                    "Рецепт с указанным идентификатором не существует."
                )
            return self.__add_recipe(recipe)

        if self.method == "DELETE":
            recipe = get_object_or_404(Recipe, id=self.pk)
            return self.__delete_recipe(recipe)


def get_shopping_cart(request):
    """Получить файл со списком покупок."""
    user = request.user
    if not user.carts.exists():
        return Response(status=BAD_REQUEST)

    ingredients = (
        RecipeIngredient.objects.filter(recipe__carts__user=request.user)
        .values(
            "ingredient__name",
            "ingredient__measurement_unit",
        )
        .annotate(ingredient_amount=Sum("amount"))
    )
    shopping_list = f"Список покупок пользователя {user}:\n"

    for ingredient in ingredients:
        name = ingredient["ingredient__name"]
        unit = ingredient["ingredient__measurement_unit"]
        amount = ingredient["ingredient_amount"]
        shopping_list += f"\n{name} - {amount}/{unit}"

    file_name = f"{user}_shopping_cart.txt"
    response = HttpResponse(shopping_list, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    return response


# TODO: Если будет время переработать. Собрать все с ингредиентами в класс
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


def check_recipe(request, obj, model):
    return (
        request
        and request.user.is_authenticated
        and model.objects.filter(recipe=obj).exists()
    )
