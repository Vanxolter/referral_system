import os
from celery.schedules import crontab
from celery.app.base import Celery
from celery.signals import after_setup_logger
import logging

from referral_system import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'referral_system.settings')

app = Celery('referral_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.log.setup_logging_subsystem(loglevel='INFO')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    print('Response: {0!r}'.format(self.response))
    print('Headers: {0!r}'.format(self.headers))
    print('Body: {0!r}'.format(self.body))
    print('Status: {0!r}'.format(self.status))
    print('Reason: {0}'.format(self.reason))
    print('-' * 80)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)


# app.conf.beat_schedule = {
#     'backup_database': {
#         'task': 'modules.services.tasks.dbackup_task',
#         'schedule': crontab(hour=0, minute=0),
#     },
#     'recalculate_reviews_hidden_ratings_for_all_task': {
#         'task': 'modules.reviews.tasks.recalculate_reviews_hidden_ratings_for_all_task',
#         'schedule': crontab(hour=0, minute=0, day_of_week=0),
#     },
#     'find_top_beatmaker_task': {
#         'task': 'modules.system.tasks.find_top_beatmaker_task',
#         'schedule': crontab(hour=0, minute=0, day_of_month=0),
#     },
# }
