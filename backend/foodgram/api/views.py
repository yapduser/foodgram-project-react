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
    RecipeSerializer,
)
from recipes.models import Tag, Ingredient, Recipe


class CustomDjoserUserViewSet(DjoserUserViewSet):
    """Получить профиль пользователя."""

    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TagViewSet(ModelViewSet):
    """Получить информацию о тегах."""

    http_method_names = ["get"]
    queryset = Tag.objects.all()
    serializer_class = TagGetSerializer
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    """Получить информацию о ингредиентах."""

    http_method_names = ["get"]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """..."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
