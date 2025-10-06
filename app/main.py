"""
Entry point for the API
"""

import logging
from fastapi import FastAPI
from app.api.v1 import jobs as jobs_v1
from app.core.logging_setup import setup_logging
from app.core.db import Base, engine 


setup_logging("api")
logger = logging.getLogger(__name__)


try:
    # db migration
    Base.metadata.create_all(bind=engine) 
    logger.info("Database tables initialized (if they didn't exist).")
except Exception as e:
    logger.error(f"Error initializing database: {e}", exc_info=True)


# FastAPI app initializer
app = FastAPI(
    title="Scheduler Microservice",
    version="1.0.0",
    description="A highly performant, scalable job scheduler built with FastAPI and Celery.",
    docs_url="/docs", 
    redoc_url="/redoc"
)


app.include_router(jobs_v1.router, prefix="/api/v1/jobs", tags=["Jobs"])


@app.get("/health", tags=["System"])
def health_check():
    """health check endpoint"""
    return {"status": "ok", "service": "Scheduler API"}
