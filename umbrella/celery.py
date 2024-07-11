import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'umbrella.settings')

app = Celery('umbrella', broker='amqp://umbrella:1234@localhost:5672/0')
app.autodiscover_tasks()