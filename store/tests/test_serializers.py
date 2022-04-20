from django.test import TestCase
from store.models import Books
from store.serializers import BooksSerializer


class BookSerializersTestCase(TestCase):
    def test_ok(self):
        book_1 = Books.objects.create(name='test1', price=550)
        book_2 = Books.objects.create(name='test2', price=330)
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {'id': book_1.id,
             'name': 'test1',
             'price': '550.00',
             'author_name': ""
             },
            {'id': book_2.id,
             'name': 'test2',
             'price': '330.00',
             'author_name': ""

            }
        ]
        self.assertEqual(expected_data, data)