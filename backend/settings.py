import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv not available


class Settings(BaseSettings):
    google_api_key: str
    text_model: str = "gemini-2.0-flash-exp"
    image_model: str = "gemini-2.5-flash-image"
    timeout_secs: int = 60
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()
