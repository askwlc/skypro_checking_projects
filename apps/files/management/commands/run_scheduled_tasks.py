from django.core.management.base import BaseCommand

from apps.files.tasks import check_file_flake8_task


class Command(BaseCommand):
    """
    Дополнительное задание со звездочкой
    в техническом задании.
    """
    help = 'Запуск задач по расписанию.'

    def handle(self, *args, **kwargs):
        check_file_flake8_task()
        self.stdout.write(self.style.SUCCESS('Successfully'))
