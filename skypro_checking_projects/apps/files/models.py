from django.db import models
from django.contrib.auth.models import User


class FileUpload(models.Model):
    """Модель загруженного файла, с полями датами загрузки и проверки, было ли редактирование."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    upload_time = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)
    check_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file.name


class FileCheckLogs(models.Model):
    """Модель хранения логов проверок."""
    STATUS_CHOICES = [
        ('waiting', 'Ожидание'),
        ('completed', 'Завершено'),
        ('error', 'Ошибка')
    ]

    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='logs')
    check_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='waiting')
    result = models.TextField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.file
