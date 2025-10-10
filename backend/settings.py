import os
from functools import lru_cache
from pathlib import Path

# Load .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv not available


class Settings:
    """Application configuration values sourced from environment variables."""

    openrouter_api_key: str
    openrouter_base_url: str
    text_model: str
    image_model: str
    timeout_secs: int

    def __init__(self) -> None:
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.text_model = os.getenv("TEXT_MODEL", "openai/gpt-3.5-turbo")
        self.image_model = os.getenv("IMAGE_MODEL", "openai/dall-e-3")
        self.timeout_secs = int(os.getenv("TIMEOUT_SECS", "60"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()
