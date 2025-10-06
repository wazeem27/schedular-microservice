"""
Schedular service: This module creates and schedule jobs
"""

import logging
from datetime import datetime, timezone

from app.db.models import Job
from app.db.repositories import JobRepository
from sqlalchemy.orm import Session
from app.services.recurrence import RecurrenceService


logger = logging.getLogger(__name__)


class SchedulerService:
    """Module handles job creation"""
    def __init__(self, db: Session, job_repo: JobRepository):
        self.db = db
        self.job_repo = job_repo
        self.recurrence_service = RecurrenceService()

    def create_and_schedule_job(self, job_data) -> Job:
        """Method handles the job creation and next run time calculation"""
        initial_next_run = self.recurrence_service.calculate_next_run(
            schedule_interval=job_data.schedule_interval,
            schedule_params=job_data.schedule_params,
            last_run_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        
        job_data_dict = job_data.model_dump()
        job_data_dict['next_run_at'] = initial_next_run
        
        try:
            new_job = self.job_repo.create(job_data_dict) 
            
            logger.info(f"Successfully created job: {new_job.name}. Initial run at: {initial_next_run}")
            return new_job
            
        except Exception as e:
            # if any of the component fail; then rollback the system
            logger.error(f"Failed to create job {job_data.name}. Error: {e}")
            raise ValueError(f"Failed to configure job: {e}") 
