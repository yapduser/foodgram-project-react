from djoser.serializers import UserCreateSerializer


class UserCreationSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя.

    Переопределяет порядок полей для Djoser.
    """

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
