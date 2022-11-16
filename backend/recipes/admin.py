from django.contrib import admin

from .models import Tag, Ingredient, Recipe, IngredientRecipe, Cart, Favorite


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'colour',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'tags', 'name',
        'text', 'cooking_time', 'ingredients', 'pub_date',
    )
    search_fields = ('name', 'author', 'tags',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-пусто-'

    def total_favorits(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    total_favorits.short_description = 'Успешно добавлено в избранное :)'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
