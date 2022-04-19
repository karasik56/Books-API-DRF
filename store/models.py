from django.db import models


class  Books(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название книги')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    author_name = models.CharField(max_length=255, default='', verbose_name='Автор')

    def __str__(self):
        return f'{self.name}'

