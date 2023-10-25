from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Subscribe,
    Tag,
    User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    list_display_links = ("username",)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "author")
    search_fields = ("user", "author")
    list_filter = ("user", "author")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color", "slug")
    search_fields = ("name", "slug")
    list_display_links = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    list_display_links = ("name",)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "favorites_amount")
    search_fields = ("name", "author")
    list_filter = ("name", "author", "tags")
    list_display_links = ("name",)
    inlines = (RecipeIngredientInline,)

    def favorites_amount(self, obj):
        return obj.favorites.count()

    favorites_amount.short_description = "Добавлено в избранное"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    search_fields = ("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    search_fields = ("user", "recipe")
