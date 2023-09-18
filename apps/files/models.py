from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class FileUpload(models.Model):
    """Модель загруженного файла, с полями датами загрузки и проверки, было ли редактирование."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)
    check_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Проверка замены файла."""
        if self.pk:
            orig = FileUpload.objects.get(pk=self.pk)
            if orig.file != self.file:
                self.is_new = True
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.file.name)


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
        return str(self.file)


@receiver(post_delete, sender=FileUpload)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)