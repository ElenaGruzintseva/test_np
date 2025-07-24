import csv
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from books.models import Author


class Command(BaseCommand):
    help = 'Загрузка авторов из CSV-файла'

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR) / 'books' / 'data' / 'authors.csv'

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                created_count = 0

                for row in reader:
                    _, created = Author.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'date_of_birth': row['date_of_birth'],
                            'autobiography': row['autobiography'],
                        }
                    )
                    if created:
                        created_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Загрузка авторов завершена! '
                    f'Создано: {created_count} авторов.'
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {csv_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке: {e}')
            )
