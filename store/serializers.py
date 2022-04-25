from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from store.models import Books, UserBookRelation


class BooksSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    price_discount = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(default='', source='owner.username', read_only=True)

    class Meta:
        model = Books
        fields = ('id', 'name', 'price', 'discount', 'author_name',
                  'annotated_likes', 'rating', 'price_discount', 'owner_name')


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmark', 'rate',)
