from celery import Celery
from datetime import timedelta
from katie.managers.credentials_manager import CredentialsManager

celery_app = Celery('katie',
              broker='amqp://localhost//',
              include=['katie.tasks.fetch_emails'])

celery_app.conf.update(
  timezone='UTC',
  beat_schedule={
    'fetch-emails-every-10-seconds': {
      'task': 'katie.tasks.fetch_emails.fetch_emails',
      'schedule': timedelta(seconds=10),
    },
  }
)