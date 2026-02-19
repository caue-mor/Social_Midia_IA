from pydantic_settings import BaseSettings
from pydantic import model_validator
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AgenteSocial API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_SECRET_KEY: str = ""

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Postgres (AGNO Memory + Storage — conexao direta ao Supabase)
    DATABASE_URL: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://social-midia-ia.vercel.app",
    ]

    # Instagram Graph API
    INSTAGRAM_ACCESS_TOKEN: str = ""
    INSTAGRAM_BUSINESS_ACCOUNT_ID: str = ""

    # YouTube Data API
    YOUTUBE_API_KEY: str = ""

    # Email (Resend)
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@agentesocial.com"

    # Storage
    MAX_UPLOAD_SIZE_MB: int = 50

    # JWT
    SUPABASE_JWT_SECRET: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @model_validator(mode="after")
    def validate_required_settings(self):
        if self.ENVIRONMENT == "test":
            return self
        missing = []
        if not self.SUPABASE_URL:
            missing.append("SUPABASE_URL")
        if not self.SUPABASE_KEY:
            missing.append("SUPABASE_KEY")
        if not self.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
