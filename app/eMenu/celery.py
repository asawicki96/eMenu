from celery import Celery
from eMenu.schedule import schedule
from django.apps import apps
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eMenu.settings')

# Initialise celery app instance
app = Celery('eMenu')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

app.conf.beat_schedule = schedule
