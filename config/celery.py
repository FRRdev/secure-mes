import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('secure_mes')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'refresh_ck_every_5_min': {
        'task': 'src.neuro_base.tasks.refresh_all_current_key',
        'schedule': crontab(minute='*/5'),
    },
}
