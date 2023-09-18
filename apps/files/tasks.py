import logging
import subprocess
from datetime import datetime
from subprocess import CompletedProcess
from typing import Optional, Tuple

from celery import shared_task
from decouple import config
from django.core.cache import cache
from django.core.mail import send_mail

from apps.files.models import FileCheckLogs, FileUpload

logger = logging.getLogger('apps')


@shared_task
def check_file_flake8_task() -> None:
    """Celery задача для проверки flake8 файлов и отправки уведомлений."""
    new_files = FileUpload.objects.filter(is_new=True)
    logger.info("Начата проверка новых файлов.")

    for file_upload in new_files:
        file_path = file_upload.file.path
        result = run_flake8(file_path)
        if not result:
            continue

        log = create_file_check_log(file_upload, result)
        update_file_upload(file_upload)

        send_notification_email(file_upload, log, result)


def run_flake8(file_path: str) -> Optional[CompletedProcess]:
    """Запуск проверки Flake8."""
    try:
        return subprocess.run(['flake8', file_path],
                              capture_output=True, text=True)
    except Exception as e:
        logger.error(f"Ошибка при проверке Flake8: {e}")
        return None


def create_file_check_log(file_upload: FileUpload,
                          result: CompletedProcess) -> FileCheckLogs:
    """Создает лог проверки файла."""
    status = 'completed' if result.returncode in [0, 1] else 'error'
    return FileCheckLogs.objects.create(
        file=file_upload,
        status=status,
        result=result.stdout
    )


def update_file_upload(file_upload: FileUpload) -> None:
    """Обновление FileUpload после проверки."""
    file_upload.is_new = False
    file_upload.check_time = datetime.now()
    file_upload.save()


def send_notification_email(file_upload: FileUpload, log: FileCheckLogs,
                            result: CompletedProcess) -> None:
    """Отправка сообщения о результатах проверки."""
    email_count, email_timestamp = get_email_cache_data()

    if email_count >= 50:
        return

    subject = 'Результаты проверки файла по flake8.'
    message = compose_email_message(file_upload, result)
    from_email = config('DEFAULT_FROM_EMAIL')

    try:
        send_mail(subject, message, from_email,
                  [file_upload.user.email], fail_silently=False)
        log.notification_sent = True
        log.save()
        update_email_cache(email_count, email_timestamp)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


def get_email_cache_data() -> Tuple[int, Optional[datetime]]:
    """Получение данный кэша о количестве писем."""
    return cache.get('email_count', 0), cache.get('email_timestamp', None)


def compose_email_message(file_upload: FileUpload,
                          result: CompletedProcess) -> str:
    """Составляет почтовое сообщение о результатах проверки."""
    if result.stdout.strip():
        return f'Файл: {file_upload.file.name}: {result.stdout}'
    return f'Файл: {file_upload.file.name}: прошел проверку. Ошибок нет.'


def update_email_cache(email_count: int,
                       email_timestamp: Optional[datetime]) -> None:
    """Обновляет количество отправленных писем и временную метку."""
    current_time = datetime.now()
    if email_timestamp and (current_time - email_timestamp).seconds >= 3600:
        email_count = 0
        cache.delete('email_timestamp')
    cache.set('email_count', email_count + 1, 3600)
    if not email_timestamp:
        cache.set('email_timestamp', current_time, 3600)
