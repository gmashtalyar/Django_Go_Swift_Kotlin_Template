import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTemplate.settings")
app = Celery("WebTemplate")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'do-something-every-night': {
        'task': 'main_app.tasks.some_night_task_XXXXXX',
        'schedule': crontab(hour=1, minute=0),  # day_of_week='tue'
    },
}
