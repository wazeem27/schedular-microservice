"""
Module defining the structure and validation of scheduled jobs.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class JobBase(BaseModel):
    name: str = Field(...)
    task_name: str = Field(
        ...,
        description="The registered Celery task name."
    )
    schedule_interval: str = Field(
        ...,
        description="Type of schedule: 'crontab' or 'interval'"
    )
    schedule_params: Dict[str, Any] = Field(
        ...,
        description=(
            "Parameters for crontab (minute, hour, day_of_month, month_of_year, day_of_week) "
            "or interval (seconds, minutes, hours, days)."
        )
    )
    task_args: Optional[Dict[str, Any]] = Field(
        None,
        description="Arguments passed to the Celery task. Must contain 'positional' (List) and 'keyword' (Dict) keys."
    )


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    id: int
    status: str
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }