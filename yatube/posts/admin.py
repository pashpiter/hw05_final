from django.contrib import admin
from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    # Поля отражаемые в admin.py
    list_display: list = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields: list = ('text',)  # Интерфейс поиска
    list_filter: list = ('pub_date',)  # Фильтр по дате
    empty_value_display: str = '-пусто-'  # Если пустое значение
    list_editable: list = ('group',)  # Добавление изменения группы


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
