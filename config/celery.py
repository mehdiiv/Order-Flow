import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-pending-orders-every-10-seconds': {
        'task': 'orders.tasks.check_pending_orders',
        'schedule': 10.0,
    },
}