from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DevSocialPlatformProject.settings')

app = Celery('DevSocialPlatformProject')





app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'delete-expired-posts-every-minute': {
        'task': 'devsearchey.tasks.delete_expired_posts',
        'schedule': crontab(minute='*'),  
    },
}