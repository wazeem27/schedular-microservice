"""Initialization and configuration for the Celery application."""
from celery import Celery
from app.core.config import settings
from app.core.logging_setup import setup_logging

setup_logging("beat")

# Celery application initialization
celery_app = Celery(
    "scheduler",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.config_from_object('celeryconfig')  # load config


import app.tasks.jobs
import app.tasks.scheduler 


celery_app.autodiscover_tasks(['app'])