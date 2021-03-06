from collections import OrderedDict

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, F
from django.test import TestCase
from store.models import Books, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializersTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        book_1 = Books.objects.create(name='test1', price=550, author_name='author1', discount=100)
        book_2 = Books.objects.create(name='test2', price=330, author_name='author2', discount=100)
        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=5)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=2)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Books.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            price_discount=F('price')-F('discount')).order_by('id')

        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'test1',
                'price': '550.00',
                'discount': '100.00',
                'author_name': 'author1',
                'annotated_likes': 3,
                'rating': '4.33',
                'price_discount': '450.00'

            },
            {
                'id': book_2.id,
                'name': 'test2',
                'price': '330.00',
                'discount': '100.00',
                'author_name': 'author2',
                'annotated_likes': 2,
                'rating': '2.50',
                'price_discount': '230.00'
            },

        ]
        print(expected_data)
        print(data)
        self.assertEqual(expected_data, data)
