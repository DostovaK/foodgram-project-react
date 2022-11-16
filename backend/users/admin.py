from django.contrib import admin

from models import Subscription  # , User


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
#     search_fields = ('username', 'email')
#     list_filter = ('username', 'email')
#     empty_value_display = '-пусто-'
