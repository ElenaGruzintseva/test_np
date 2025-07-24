from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    # Поле preface может быть очень большим, поэтому не загружаем его
    # для списка книг
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'year_of_publication']
        read_only_fields = ['id']


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year_of_publication', 'preface']
