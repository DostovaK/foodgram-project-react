from django.contrib.auth import get_user_model
from django_filters.rest_framework import CharFilter, FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(SearchFilter):
    name = CharFilter(field_name="name", lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='if_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='if_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)

    def if_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def if_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(cart__user=self.request.user)
        return
