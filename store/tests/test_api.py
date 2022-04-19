from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Books
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book_1 = Books.objects.create(name = 'test1', price = 550, author_name='author_1')
        self.book_2 = Books.objects.create(name='test2', price=330, author_name='author_2')
        self.book_3= Books.objects.create(name='test3 author_1', price=300, author_name='author_3')

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
