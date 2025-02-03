try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings



class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()