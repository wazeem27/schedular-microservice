"""
Module consists of Celery task types that can be performed.
"""
from app.tasks import celery_app
from datetime import datetime
import time
import logging
import os

logger = logging.getLogger(__name__)

@celery_app.task(name='app.tasks.jobs.send_email', bind=True)
def send_email(self, job_id: int):
    """Dummy task for sending an email notification."""
    logger.info(f"Task {self.request.id}: Starting email notification for job ID: {job_id}")
    time.sleep(3) # Simulate time taken by just wait for few seconds
    logger.info(f"Task {self.request.id}: Email notification sent for job ID: {job_id} at {datetime.now()}")


@celery_app.task(name='app.tasks.jobs.log_heartbeat', bind=True)
def log_heartbeat(self, *args, **kwargs):
    """
    This task will create a file in the current dir if doesn't exist and append a
    timestamdped line used to verify that the celery schedular is runnig perodic tasks.
    """
    job_id = args[0] if args else None
    filename = 'scheduler_heartbeat.txt'
    if len(args) > 1:
        if isinstance(args[1], str):
            filename = args[1]
        else:
            logger.warning(
                f"Job ID {job_id}: Expected filename (str) at args[1] but got {type(args[1])}. Using default filename."
            )

    file_path = os.path.join(os.getcwd(), filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_line = (
        f"[{timestamp}] Task ID: {self.request.id} | Job ID: {job_id} | "
        f"File: {filename} | Args: {args}, Kwargs: {kwargs}.\n"
    )
    
    try:
        with open(file_path, 'a') as f:
            f.write(log_line)
        logger.info(f"Task {self.request.id}: Successfully logged heartbeat to {file_path}")
        
    except Exception as e:
        logger.error(
            f"Task {self.request.id}: Failed to write message to file: {e}", exc_info=True
        )
