from rest_framework.viewsets import ModelViewSet

from store.models import Books
from store.serializers import BooksSerializer


class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
