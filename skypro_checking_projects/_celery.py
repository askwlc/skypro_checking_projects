from __future__ import absolute_import, unicode_literals
from celery import Celery

import os

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skypro_checking_projects.settings')

app = Celery('skypro_checking_projects')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
