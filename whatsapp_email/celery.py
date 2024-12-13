from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODDULE', 'whatsapp_email.settings')

app = Celery('whatsapp_email')
app.config_from_object('django.conf:settings', name = 'CELERY')
app.autodiscover_tasks()
