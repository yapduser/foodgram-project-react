from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import User, Tag, Ingredient, Recipe, RecipeIngredient
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
    """Сериализатор получения информации о пользователе."""

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


class TagGetSerializer(serializers.ModelSerializer):
    """Сериализатор получения информации о тегах."""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор работы с ингредиентами."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов в рецепте."""

    name = serializers.StringRelatedField(
        source="ingredient",
        read_only=True,
    )
    measurement_unit = serializers.StringRelatedField(
        source="ingredient.measurement_unit",
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор работы с ингредиентами."""

    tags = TagGetSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source="recipe_ingredients"
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
