import os

from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from django.utils.timezone import now

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Tashkent')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-deadline-every-5-minutes': {
        'task': 'kanban.tasks.check_deadlines',
        'schedule': crontab(minute='*/5'),
    },
}
