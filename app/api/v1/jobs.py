"""
Module defines all API definition
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.db.repositories import JobRepository
from app.services.scheduler import SchedulerService
from app.schemas.job import JobRead, JobCreate
from typing import List
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


def get_scheduler_service(db: Session = Depends(get_db)) -> SchedulerService:
    job_repo = JobRepository(db)
    return SchedulerService(db, job_repo)

@router.get("/", response_model=List[JobRead], summary="List all scheduled jobs")
def list_jobs(service: SchedulerService = Depends(get_scheduler_service)):
    """ListView of a job"""
    logger.info("API call: Listing all jobs.")
    jobs = service.job_repo.get_all()
    return jobs

@router.get("/{job_id}", response_model=JobRead, summary="Retrieve a specific job by ID")
def get_job(job_id: int, service: SchedulerService = Depends(get_scheduler_service)):
    """Detail view of a Job"""
    logger.info(f"API call: Retrieving job ID {job_id}.")
    job = service.job_repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED, summary="Create a new job")
def create_job(job: JobCreate, service: SchedulerService = Depends(get_scheduler_service)):
    """Create view of a job"""
    logger.info(f"API call: Creating new job '{job.name}'.")
    try:
        new_job = service.create_and_schedule_job(job)
        return new_job
    except ValueError as e:
        logger.error(f"Validation error during job creation: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during job creation: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create and schedule job due to an internal error.")
