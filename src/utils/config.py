from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    postgres_database: str
    postgres_password: str
    postgres_user: str
    postgres_hostname: str
    postgres_raw_db: str
    postgres_std_db: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
