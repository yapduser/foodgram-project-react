from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import User, Subscribe


class UserSignUpSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя.

    Переопределяет порядок полей для Djoser.
    """

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class UserGetSerializer(UserSerializer):
    """Сериализатор для получения информации о пользователях."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        return (
            request.user.is_authenticated
            and Subscribe.objects.filter(
                user=request.user, author=obj
            ).exists()
        )
