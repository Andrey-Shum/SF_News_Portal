import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
       'send_weekly_news': {
           'task': 'news.tasks.send_weekly_news',
           'schedule': crontab(day_of_week='mon', hour=8),
       },
   }
