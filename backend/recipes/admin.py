from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag, IngredientRecipe)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)
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
        'id', 'author', 'name',
        'text', 'cooking_time', 'pub_date',
    )
    search_fields = ('name', 'author', 'tags',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-пусто-'
    inlines = (IngredientInline,)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'
