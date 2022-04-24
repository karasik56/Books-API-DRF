from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from store.models import Books, UserBookRelation


class BooksSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Books
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotated_likes', 'rating')

    def get_likes_count(self, instanse):
        return UserBookRelation.objects.filter(book=instanse, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmark', 'rate',)
