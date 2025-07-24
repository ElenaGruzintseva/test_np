import csv
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from books.models import Author, Book


class Command(BaseCommand):
    help = 'Загрузка книг из CSV-файла'

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR) / 'books' / 'data' / 'books.csv'

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                created_count = 0
                skipped_count = 0

                for row in reader:
                    title = row['title'].strip()
                    author_name = row['author'].strip()
                    year = int(row['year_of_publication'])
                    preface = row['preface'].strip()
                    cover_filename = row.get('cover', '').strip()

                    try:
                        author = Author.objects.get(name=author_name)
                    except Author.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Автор не найден: "{author_name}" для книги "{title}". Пропущено.'
                            )
                        )
                        skipped_count += 1
                        continue
                    except Author.MultipleObjectsReturned:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Найдено несколько авторов: "{author_name}". Берём первого.'
                            )
                        )
                        author = Author.objects.filter(name=author_name).first()

                    if Book.objects.filter(title=title).exists():
                        skipped_count += 1
                        continue

                    cover_path = None
                    if cover_filename:
                        cover_path = f'books/covers/{cover_filename}'

                    try:
                        book = Book.objects.create(
                            title=title,
                            author=author,
                            year_of_publication=year,
                            preface=preface,
                            cover=cover_path
                        )
                        created_count += 1
                    except ValidationError as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Ошибка валидации при создании книги "{title}": {e}'
                            )
                        )
                        skipped_count += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Ошибка при создании книги "{title}": {e}'
                            )
                        )
                        skipped_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Загрузка книг завершена! '
                    f'Создано: {created_count}, Пропущено: {skipped_count}.'
                )
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {csv_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при чтении файла: {e}')
            )
