"""
Module for calculating the next scheduled execution time for jobs
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from croniter import croniter


logger = logging.getLogger(__name__)


class RecurrenceService:
    """Calculates the next execution timestamp"""

    def calculate_next_run(
        self,
        schedule_interval: str,
        schedule_params: Dict[str, Any],
        last_run_at: Optional[datetime] = None
    ) -> datetime:
        """
        Calculates the next run time. 
        """
        base_time = last_run_at if last_run_at else datetime.now(timezone.utc).replace(tzinfo=None)
        
        if schedule_interval == 'interval':
            return self._calculate_interval(schedule_params, base_time)
            
        elif schedule_interval == 'crontab':
            return self._calculate_crontab(schedule_params, base_time)
            
        else:
            raise ValueError(f"Unsupported schedule interval type: {schedule_interval}")

    def _calculate_interval(self, params: Dict[str, Any], base_time: datetime) -> datetime:
        """Calculates next run for an interval schedule"""
        period, every = next(iter(params.items()))
        
        if period == 'seconds':
            delta = timedelta(seconds=every)
        elif period == 'minutes':
            delta = timedelta(minutes=every)
        elif period == 'hours':
            delta = timedelta(hours=every)
        elif period == 'days':
            delta = timedelta(days=every)
        else:
            raise ValueError(f"Invalid interval period: {period}")

        return base_time + delta

    def _calculate_crontab(self, params: Dict[str, Any], base_time: datetime) -> datetime:
        """Calculates next run for a crontab schedule."""
        minute = str(params.get('minute', '*'))
        hour = str(params.get('hour', '*'))
        day_of_month = str(params.get('day_of_month', '*'))
        month_of_year = str(params.get('month_of_year', '*'))
        day_of_week = str(params.get('day_of_week', '*'))

        cron_string = f"{minute} {hour} {day_of_month} {month_of_year} {day_of_week}"
        
        try:
            itr = croniter(cron_string, start_time=base_time)
            return itr.get_next(datetime)
        except Exception as e:
            raise ValueError(f"Invalid cron expression '{cron_string}': {e}")
