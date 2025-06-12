import os 

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.base')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-1-minunts': {
        'task': 'technews.news.tasks.run_spider',
        'schedule': 60.0,
    },
}
app.conf.timezone = 'Asia/Tehran'