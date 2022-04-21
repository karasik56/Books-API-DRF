from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase
from store.models import Books
from store.serializers import BooksSerializer


class BookSerializersTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Books.objects.create(name='test1', price=550, author_name='', )
        book_2 = Books.objects.create(name='test2', price=330,author_name='',)
        data = BooksSerializer([self.book_1], many=True).data
        expected_data = [OrderedDict([('id', self.book_1.id), ('name', 'test1'), ('price', '550.00'), ('author_name', ''), ('owner', None)])]
        print(data)
        print(expected_data)
        self.assertEqual(expected_data, data)