"""
Repository layer for managing scheduled job data persistence.
"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.models import Job
from app.schemas.job import JobCreate


logger = logging.getLogger(__name__)


class JobRepository:
    """Implements the Repository Pattern for Job CRUD operations."""
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self) -> List[Job]:
        logger.debug("Fetching all jobs from DB.")
        return self.db.query(Job).all()
        
    def get_by_id(self, job_id: int) -> Optional[Job]:
        logger.debug(f"Fetching job with ID: {job_id}.")
        return self.db.query(Job).filter(Job.id == job_id).first()
        
    def create(self, job_data: Dict[str, Any]) -> Job:
        """
        method for creating a new job entry
        """
        logger.info(f"Creating new job entry: {job_data.get('name')}")
        db_job = Job(**job_data)
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job
