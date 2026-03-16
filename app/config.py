from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Agentic Test System"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "agentic_testing"

    # LLM
    GROQ_API_KEY: str | None = None
    LMSTUDIO_URL: str = "http://localhost:1234"

    # Vector DB
    CHROMA_PATH: str = "data/chroma_db"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()