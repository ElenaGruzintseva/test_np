from rest_framework import filters
from django_filters import rest_framework as django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    # Кастомная фильтрация для более сложной фильтрации по автору и году.
    author = django_filters.NumberFilter(field_name='author__id')
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='istartswith'
    )
    year = django_filters.NumberFilter(field_name='year_of_publication')
    year_min = django_filters.NumberFilter(
        field_name='year_of_publication',
        lookup_expr='gte',
        label='From year'
    )
    year_max = django_filters.NumberFilter(
        field_name='year_of_publication',
        lookup_expr='lte',
        label='To year'
    )

    class Meta:
        model = Book
        fields = ['author', 'author_name', 'year', 'year_min', 'year_max']


class BookOrderingFilter(filters.OrderingFilter):
    # Явно указываем разрешённые поля сортировки для индексированных полей.
    # Для поля year_of_publication ищем по year - так проще.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ordering_fields = [
            ('title', 'title'),
            ('-title', '-title'),
            ('year_of_publication', 'year'),
            ('-year_of_publication', '-year')
        ]
