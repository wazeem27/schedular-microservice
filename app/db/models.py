"""Job database model"""

from sqlalchemy import Column, Integer, String, DateTime, func, Index
from sqlalchemy.dialects.postgresql import JSONB
from app.core.db import Base
from sqlalchemy import UniqueConstraint


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    task_name = Column(String, nullable=False)
    
    schedule_interval = Column(String(64), nullable=False)
    schedule_params = Column(JSONB, nullable=False)
    task_args = Column(JSONB, default={}, nullable=True)
    
    status = Column(String(32), default='active', index=True)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Job(id={self.id}, name={self.name}, status={self.status})>"
