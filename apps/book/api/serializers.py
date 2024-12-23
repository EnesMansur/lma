from rest_framework import serializers
from book.models import Book, BookEdition


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_date", "isbn", "genre", "quantity"]


class BookEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEdition
        # fields = ["book__title", "book__author", "book__publication_date", "book__isbn", "book__genre",
        #          "book__quantity", "edition_number", "published_year", "quantity", "format"]
        fields = ["book", "edition_number", "published_year", "quantity", "format"]


class BookListSerilazer(serializers.Serializer):
    page = serializers.IntegerField(default=0)
    limit = serializers.IntegerField(default=50, max_value=100)
    title = serializers.CharField(max_length=64, required=False)
    author = serializers.CharField(max_length=64, required=False)
    isbn = serializers.CharField(max_length=32, required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)


class BookBulkDummySerilazer(serializers.Serializer):
    bulk_size = serializers.IntegerField(required=True)
