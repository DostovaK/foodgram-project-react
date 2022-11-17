from rest_framework import serializers
from recipes.models import (Tag, Ingredient, Recipe,
                            IngredientRecipe, Cart, Favorite)
from drf_extra_fields.fields import Base64ImageField
from .utils import is_in_favorites_or_shopping_list
# from users.models import 


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)
        validators = serializers.UniqueTogetherValidator(
            queryset=IngredientRecipe.objects.all(),
            fields=('recipe', 'ingredient')
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField('get_ingredients')
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        record = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(record, many=True).data

    def get_is_favorited(self, obj):
        return is_in_favorites_or_shopping_list(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return is_in_favorites_or_shopping_list(self, obj, Cart)