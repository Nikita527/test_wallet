from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    app_name: str = "fastapi-test-wallet-service"
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    api_prefix: str = "/api"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
