"""
Module act like database gateway for the python script
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

# Base class for models
Base = declarative_base()


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()