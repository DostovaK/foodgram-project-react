from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                           ShoppingCartViewSet, TagViewSet)
from users.views import UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<int:id>/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'delete'}
    )),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartViewSet.as_view(
        {'post': 'create', 'delete': 'delete'}
    )),
]
