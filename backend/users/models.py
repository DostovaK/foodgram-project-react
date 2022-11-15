# from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth import get_user_model  # временно
User = get_user_model()  # временно

'''class User(AbstractUser):
    """User model."""
    # USER = 'user'
    # MODERATOR = 'moderator'
    # ADMIN = 'admin'
    # ROLE_CHOICES = (
    #     (USER, 'user'),
    #     (MODERATOR, 'moderator'),
    #     (ADMIN, 'admin'),
    # )
    email = models.EmailField(
        'e-mail',
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Введите ваш адрес электронной почты'
    )
    username = models.CharField(
        'Юзернейм пользователя',
        max_length=150,
        unique=True,
        verbose_name='Юзернейм',
        help_text='Введите юзернейм'
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        verbose_name='Имя',
        help_text='Введите ваше имя'
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите вашу фамилию'
    )

    def __str__(self) -> str:
        return self.username


    # @property
    # def is_moderator(self):
    #     return self.role == self.MODERATOR

    # @property
    # def is_admin(self):
    #     return self.role == self.ADMIN
'''


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_follower'
            )
        ]

    def __str__(self):
        return f'{self.user}, {self.author}'
