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
from api.services import RecipeProcessor, get_shopping_cart
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
        recipe_processor = RecipeProcessor(
            serializer_name=FavoriteSerializer,
            model=Favorite,
            request=request,
            pk=pk,
            err_msg="Рецепт отсутствует в избранном.",
        )
        return recipe_processor.execute()

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        recipe_processor = RecipeProcessor(
            serializer_name=ShoppingCartSerializer,
            model=ShoppingCart,
            request=request,
            pk=pk,
            err_msg="Рецепт отсутствует в списке покупок.",
        )
        return recipe_processor.execute()

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        return get_shopping_cart(request)
