from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Tags model."""
    name = models.CharField(
        max_length=200,
        db_index=True,
        unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        max_length=7,
        format='hex',
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        """Model's meta parameters."""
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        """String representation method."""
        return self.name


class Ingredient(models.Model):
    """Ingredients model."""
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta():
        """Model's meta parameters."""
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        """String representation method."""
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Recipes model."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Рецепт')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='Время приготовления должно быть более одной минуты.'
        )],
        verbose_name='Время приготовления'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания рецепта'
    )

    class Meta:
        """Model's meta parameters."""
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        """String representation method."""
        return self.name


class IngredientRecipe(models.Model):
    """Ingredients of recipe model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='Слишком мало ингредиентов.'
        )],
        verbose_name='Количество продукта'
    )

    class Meta:
        """Model's meta parameters."""
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredients_amount_for_recipe'
            )
        ]

    def __str__(self) -> str:
        """String representation method."""
        return f'{self.ingredient.name}, {self.recipe.name}'


class Favorite(models.Model):
    """Adding recipe to favourites model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        """Model's meta parameters."""
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favirite'
            )
        ]

    def __str__(self) -> str:
        """String representation method."""
        return f'{self.recipe}, {self.user}'


class ShoppingCart(models.Model):
    """Shopping cart model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_list',
    )

    class Meta:
        """Model's meta parameters."""
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        default_related_name = 'shopping_list'

    def __str__(self) -> str:
        """String representation method."""
        return f'{self.user}, {self.recipe}'
