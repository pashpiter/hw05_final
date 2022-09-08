from django.contrib import admin
from .models import Group, Post, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display: list = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields: list = ('text',)  # Интерфейс поиска
    list_filter: list = ('pub_date',)  # Фильтр по дате
    empty_value_display: str = '-пусто-'  # Если пустое значение
    list_editable: list = ('group',)  # Добавление изменения группы


class CommentAdmin(admin.ModelAdmin):
    list_display: list = ('pk', 'post', 'author', 'text', 'created')
    search_fields: list = ('text',)
    list_filter: list = ('created',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow)
