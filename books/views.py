from rest_framework import generics, permissions
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookCreateSerializer, BookListSerializer
from .filters import BookFilter, BookOrderingFilter


class BookListView(generics.ListCreateAPIView):
    # Используем select_related для оптимизации запросов к автору
    # (избегаем N+1 проблему)
    # only() выбирает только необходимые поля - уменьшаем нагрузку на БД
    queryset = Book.objects.select_related('author').only(
        'id', 'title', 'year_of_publication', 'author__name'
    )
    filter_backends = [django_filters.DjangoFilterBackend, BookOrderingFilter]
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('author')
    serializer_class = BookCreateSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
