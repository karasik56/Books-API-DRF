from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Books, UserBookRelation


@admin.register(Books)
class BooksAdmin(ModelAdmin):
    pass


@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass
