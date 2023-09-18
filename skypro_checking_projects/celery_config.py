import os
from celery import Celery
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'skypro_checking_projects.settings')
django.setup()
app = Celery('skypro_checking_projects')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)