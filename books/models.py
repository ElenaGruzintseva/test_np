from datetime import date

from django.db import models
from django.core.exceptions import ValidationError


class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    autobiography = models.TextField()

    # Добавлено отображение года рождения, т.к. имена могут повторяться
    def __str__(self):
        return f'{self.name} ({self.date_of_birth.year})'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_index=True)
    year_of_publication = models.IntegerField(db_index=True)
    preface = models.TextField()
    cover = models.ImageField(
        'Обложка',
        upload_to='books/covers/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    def clean(self):
        current_year = date.today().year
        if self.year_of_publication > current_year:
            raise ValidationError({
                'year_of_publication':
                f'Год издания не может быть больше {current_year}.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # Иcпользуется индексация для оптимизации групповых запросов к базе данных.
    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['author', 'year_of_publication']),
        ]
