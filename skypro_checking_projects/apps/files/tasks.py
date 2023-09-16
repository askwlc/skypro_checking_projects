from celery import shared_task

from .models import FileUpload, FileCheckLogs
from .utils import check_file_flake8


@shared_task
def check_files(file_id: int):
    """Проверка загруженного файла с помощью flake8 и запись результатов в базу данных."""
    uploaded_file = FileUpload.objects.get(id=file_id)
    check_result = check_file_flake8(uploaded_file.file.path)
    FileCheckLogs.objects.create(
        file=uploaded_file,
        check_result=check_result,
        status='completed' if check_result == '' else 'error'
    )
