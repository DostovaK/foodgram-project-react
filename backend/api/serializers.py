from rest_framework import serializers
from recipes.models import (Tag, Ingredient, Recipe, TagReceipt,
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
            'cooking_time',
        )

    def get_ingredients(self, obj):
        record = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(record, many=True).data

    def get_is_favorited(self, obj):
        return is_in_favorites_or_shopping_list(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return is_in_favorites_or_shopping_list(self, obj, Cart)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            IngredientRecipe.objects.create(
                ingredient=ingredient_model,
                recipe=recipe,
                amount=amount
            )
        for tag in tags_data:
            TagReceipt.objects.create(recipe=recipe, tag=tag)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredient_data = validated_data.pop('ingredients')
        TagReceipt.objects.filter(recipe=instance).delete()
        for tag in tags_data:
            TagReceipt.objects.create(
                recipe=instance,
                tag=tag
            )
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for new_ingredient in ingredient_data:
            IngredientRecipe.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount']
            )
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance


class DemoRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return DemoRecipeSerializer(
            instance.recipe, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Этот рецерт уже был добавлен!'
            })
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return DemoRecipeSerializer(
            instance.recipe, context=context).data
