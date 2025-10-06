"""
Defines centralized logging setup
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging(service_name: str):
    """
    Centralized logging setup.
    Logs to <LOG_DIR>/<service_name>.log and console.
    """

    base_log_dir = Path(settings.LOG_DIR).resolve()
    base_log_dir.mkdir(parents=True, exist_ok=True)

    log_file = base_log_dir / f"{service_name}.log"

    log_formatter = logging.Formatter(
        f"%(asctime)s - %(name)s - %(levelname)s - (Service: {service_name}) - %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info(f"Logging setup complete for {service_name}. Log file: {log_file}")
