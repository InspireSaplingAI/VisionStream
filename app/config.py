"""
Application Configuration
==========================
Loads environment variables using pydantic-settings.

All secrets and environment-specific values are read from a .env file
(or actual environment variables in production). They are NEVER hardcoded
in source files.

pydantic-settings automatically reads values from:
  1. Actual OS environment variables (highest priority)
  2. A .env file in the project root
  3. Default values defined in the Settings class

📌 Lesson 1 Task:
    1. Add a DATABASE_URL field (PostgreSQL connection string)
    2. Add a REDIS_URL field
    3. Add an API_KEY field for simple request authentication
    4. Implement get_settings() as a cached singleton using @lru_cache
       so the .env file is only read once per process startup
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.

    Field names must exactly match the variable names in .env.example.
    """

    APP_NAME: str = "VisionStream"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # TODO (Lesson 1): Add database configuration
    # DATABASE_URL: str = "postgresql://visionstream:changeme@localhost:5432/visionstream"

    # TODO (Lesson 1): Add Redis configuration
    # REDIS_URL: str = "redis://localhost:6379/0"

    # TODO (Lesson 1): Add API key for device authentication
    # API_KEY: str = "changeme-dev-key-replace-in-production"

    class Config:
        env_file = ".env"
        case_sensitive = True


# TODO (Lesson 1): Implement a cached settings singleton
# The @lru_cache decorator ensures the Settings object is created
# only once, even though get_settings() may be called many times
# per request via FastAPI's Depends() system.
#
# @lru_cache()
# def get_settings() -> Settings:
#     return Settings()
