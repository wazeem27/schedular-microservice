"""
Module consist of function 'check_and_run_jobs` which queries database for
for active jobs that are due for execution.
"""
from app.tasks import celery_app
from app.core.db import get_db
from app.db.models import Job
from app.services.recurrence import RecurrenceService
from datetime import datetime, timezone
import logging


logger = logging.getLogger(__name__)


@celery_app.task(name='app.tasks.scheduler.check_and_run_jobs', bind=True)
def check_and_run_jobs(self):
    """
    function runs periodically (defined in celeryconfig.py), checks the database 
    for jobs ready to run, and launches them.
    """
    logger.info("Custom Scheduler check initiated.")
    
    # Instantiate the recurrence service for next run calculations
    recurrence_service = RecurrenceService()

    with next(get_db()) as db: 
        now_utc_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        
        ready_jobs = db.query(Job).filter(
            Job.status == 'active',
            Job.next_run_at <= now_utc_naive
        ).all()

        if not ready_jobs:
            logger.info("No active jobs due for execution.")
            return

        logger.info(f"Found {len(ready_jobs)} job(s) ready for execution.")

        # Process each ready job
        for job in ready_jobs:
            try:
                next_run = recurrence_service.calculate_next_run(
                    schedule_interval=job.schedule_interval,
                    schedule_params=job.schedule_params,
                    last_run_at=now_utc_naive
                )

                job.last_run_at = now_utc_naive
                job.next_run_at = next_run
                
                task_args = job.task_args.get("positional", [])
                task_kwargs = job.task_args.get("keyword", {})
                
                full_args = [job.id] + task_args

                celery_app.send_task(  # send the task to celery worker
                    job.task_name,
                    args=full_args,
                    kwargs=task_kwargs,
                    task_id=f"job-{job.id}-{now_utc_naive.strftime('%Y%m%d%H%M%S%f')}"
                ) 
                
                logger.info(f"Scheduled task '{job.task_name}' for job ID {job.id}. Next run at: {next_run}")
                
            except Exception as e:
                logger.error(f"Failed to process job ID {job.id} ({job.name}): {e}", exc_info=True)

        db.commit()  # commit job updates
