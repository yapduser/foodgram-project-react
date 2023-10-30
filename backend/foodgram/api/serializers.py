from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import User, Tag
from service.checks import check_subscribe


class UserSignUpSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

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
    """Сериализатор для получения информации о пользователе."""

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
        return check_subscribe(self.context.get("request"), obj)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о тегах."""

    class Meta:
        model = Tag
        fields = "__all__"
