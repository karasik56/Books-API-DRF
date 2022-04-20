import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Books
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Books.objects.create(name = 'test1', price = 550.00, author_name='author_1')
        self.book_2 = Books.objects.create(name='test2', price=330, author_name='author_2')
        self.book_3 = Books.objects.create(name='test3 author_1', price=300, author_name='author_3')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={
            'search': 'author_1'
        })
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_sort(self):
        url = reverse('book-list')
        response = self.client.get(url, data={
            'ordering': '-price'
        })
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={
            'price': '300.00'
        })
        serializer_data = BooksSerializer([self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Books.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "War and Piece",
            "price": "999.00",
            "author_name": "Tolstoy"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Books.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'id': self.book_1.id,
            'name': self.book_1.name,
            'price': 665.0,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(665, self.book_1.price)

    def test_delete(self):
        self.assertEqual(3, Books.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url, )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Books.objects.all().count())

    def test_get_single_book(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        response = self.client.get(url, )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Books.objects.filter(id=self.book_1.id).count())
