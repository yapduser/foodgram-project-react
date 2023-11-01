from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import IngredientFilter
from api.serializers import (
    TagGetSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateUpdateSerializer,
    FavoriteSerializer,
)
from api.utils import add_recipe, delete_recipe
from recipes.models import Tag, Ingredient, Recipe, Favorite


class CustomDjoserUserViewSet(DjoserUserViewSet):
    """Пользователь"""

    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TagViewSet(ModelViewSet):
    """Тег."""

    http_method_names = ["get"]
    queryset = Tag.objects.all()
    serializer_class = TagGetSerializer
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    """Ингредиент."""

    http_method_names = ["get"]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    # TODO: Добавить докстринг
    """Рецепт."""

    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeGetSerializer
        return RecipeCreateUpdateSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        """Работа с рецептом в избранном. Добавить/Удалить."""

        if request.method == "POST":
            try:
                recipe = Recipe.objects.get(id=pk)
            except Recipe.DoesNotExist:
                raise ValidationError(
                    "Рецепт с указанным идентификатором не существует",
                )
            return add_recipe(request, recipe, FavoriteSerializer)

        if request.method == "DELETE":
            recipe = get_object_or_404(Recipe, id=pk)
            return delete_recipe(request, Favorite, recipe)

    def shopping_cart(self):
        ...
