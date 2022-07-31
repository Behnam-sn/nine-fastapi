import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    CORS_ORIGINS: list = []

    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days

    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
