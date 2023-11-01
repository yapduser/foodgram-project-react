from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
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
    ShoppingCartSerializer,
)
from api.services import RecipeProcessor
from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart


class CustomDjoserUserViewSet(DjoserUserViewSet):
    """Пользователь."""

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
    """Рецепт."""

    queryset = Recipe.objects.all()
    recipe_processor = RecipeProcessor()

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
        err_msg = "Рецепт отсутствует в избранном."
        return self.recipe_processor.check_request_method(
            request, pk, FavoriteSerializer, Favorite, err_msg
        )

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        err_msg = "Рецепт отсутствует в списке покупок."
        return self.recipe_processor.check_request_method(
            request, pk, ShoppingCartSerializer, ShoppingCart, err_msg
        )
