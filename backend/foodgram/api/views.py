from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import TagSerializer
from recipes.models import Tag


class CustomDjoserUserViewSet(DjoserUserViewSet):
    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TagViewSet(ModelViewSet):
    """Получить информацию о тегах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ["get"]


class IngredientViewSet(ModelViewSet):
    ...


class RecipeViewSet(ModelViewSet):
    ...
