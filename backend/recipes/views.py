from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from api.filters import IngredientFilter, RecipeFilter
from api.paginator import CustomPaginator
from api.permissions import AuthorOrAdmileElseReadOnly
from api.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                             IngredientSerializer, ShowRecipeSerializer,
                             ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    """ Вывод тегов """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вывод ингредиентов """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPaginator
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вывод работы с рецептами """
    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    permission_classes = [AuthorOrAdmileElseReadOnly]
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeSerializer
        return CreateRecipeSerializer

    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).values_list(
            "ingredient__name", "ingredient__measurement_unit", "amount"
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    "measurement_unit": item[1],
                    "amount": item[2],
                }
            else:
                final_list[name]["amount"] += item[2]
        pdfmetrics.registerFont(
            TTFont("caviar-dreams", "data/caviar-dreams.ttf", "UTF-8")
        )
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            "attachment; " 'filename="shopping_list.pdf"'
        )
        page = canvas.Canvas(response)
        page.setFont("caviar-dreams", size=20)
        page.drawString(200, 800, "Список покупок")
        page.setFont("caviar-dreams", size=16)
        height = 700
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(
                75,
                height,
                (
                    f'{i}. {name} - {data["amount"]} '
                    f'{data["measurement_unit"]}'
                ),
            )
            height -= 25
        page.showPage()
        page.save()
        return response


class FavCartBasicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data_my = {
            'user': request.user.id,
            'recipe': kwargs.get('id')

        }
        serializer = self.get_serializer(data=data_my)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(serializer.validated_data)

    def delete(self, request, *args, **kwargs):
        favorite = kwargs.get('id')
        self.model.objects.filter(
            user=request.user.id,
            recipe=favorite
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(FavCartBasicViewSet):
    """ Вывод избранных рецептов  """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    model = Favorite


class ShoppingCartViewSet(FavCartBasicViewSet):
    """ Вывод списка покупок """
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    model = ShoppingCart
