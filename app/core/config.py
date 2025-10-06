"""
Module defines settings contains db information and env details
"""

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    LOG_DIR: str = Field(default="./logs") 

    @property
    def DATABASE_URL(self) -> str:
        """Construct SQLAlchemy database URL."""
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()
