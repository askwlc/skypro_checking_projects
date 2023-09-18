from datetime import datetime

from celery import shared_task
import subprocess
from django.core.mail import send_mail
from decouple import config


@shared_task
def check_file_flake8_task():
    from apps.files.models import FileUpload, FileCheckLogs
    new_files = FileUpload.objects.filter(is_new=True)

    for file_upload in new_files:
        file_path = file_upload.file.path
        result = subprocess.run(['flake8', file_path], capture_output=True, text=True)

        FileCheckLogs.objects.create(
            file=file_upload,
            status='completed' if result.returncode == 0 else 'error',
            result=result.stdout
        )

        file_upload.is_new = False
        file_upload.check_time = datetime.now()
        file_upload.save()
        subject = 'Результаты проверки файла по flake8.'
        if result.stdout.strip():
            message = f'Файл: {file_upload.file.name}: {result.stdout}'
        else:
            message = f'Файл: {file_upload.file.name}: прошел проверку. Ошибок нет.'
        from_email = config('DEFAULT_FROM_EMAIL')
        last_log = file_upload.logs.last()
        if not last_log.notification_sent:
            try:
                send_mail(subject, message, from_email, [file_upload.user.email], fail_silently=False)
                last_log.notification_sent = True
                last_log.save()
            except Exception as e:
                print(f"Failed to send email: {e}")

