from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.conf import settings

User = get_user_model()
# from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=200
    )
    color = ColorField(
        'Цвет',
        format='hex',
        max_length=7
    )
    slug = models.SlugField(
        'Адрес',
        unique=True,
        max_length=200
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        through='TagRecipe'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Рецепт'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(1, message='Время готовки должно быть больше.')
        )
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientRecipe',
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания рецепта',
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:settings.SYMBOLS_SHOWN]


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_amount'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_amount'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество продукта',
        validators=MinValueValidator(1, message='Слишком мало ингредиентов.')
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredients_amount_for_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name}, {self.recipe.name}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user}, {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favirite'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.user}'
