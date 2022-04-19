from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Books


@admin.register(Books)
class BooksAdmin(ModelAdmin):
    pass