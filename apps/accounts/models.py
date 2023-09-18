from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class EmailConfirmation(models.Model):
    """Модель email верификации."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=64, unique=True)
    confirmed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('confirm_email', args=[str(self.confirmation_code)])
