from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings, like the exchange API key."""
    EXCHANGE_API_KEY: str

    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"

settings = Settings()
