from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomDjoserUserViewSet(DjoserUserViewSet):
    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TagViewSet(ModelViewSet):
    ...


class IngredientViewSet(ModelViewSet):
    ...


class RecipeViewSet(ModelViewSet):
    ...
