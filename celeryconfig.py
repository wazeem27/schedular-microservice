"""
Celery confirguration
"""
import os
from app.core.config import settings
from celery.schedules import timedelta, crontab

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

timezone = 'UTC'
enable_utc = True


beat_schedule = {
    'run-custom-scheduler-every-10-seconds': {
        'task': 'app.tasks.scheduler.check_and_run_jobs',
        'schedule': timedelta(seconds=10), 
        'args': (), 
    },
    'log-scheduler-heartbeat-every-minute': {
        'task': 'app.tasks.jobs.log_heartbeat',
        'schedule': crontab(minute='*'),
    }
}

task_acks_late = True
task_reject_on_worker_lost = True
