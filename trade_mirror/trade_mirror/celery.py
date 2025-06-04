from celery.schedules import crontab
import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trade_mirror.settings")
django.setup()

app = Celery('trade_mirror')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-txs-every-5-min': {
        'task': 'core.tasks.check_new_transactions',
        'schedule': crontab(minute='*/1'),
    },
}
