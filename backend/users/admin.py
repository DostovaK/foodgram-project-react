from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin zone settings."""
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'last_name')
    ordering = ('username', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Followers admin zone settings."""
    list_display = ('user', 'author',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
