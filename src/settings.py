import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PORT: int = 8000

    CONFIG_FILE_PATH: str = 'config.yaml'

settings = (
    Settings(_env_file=".env", _env_file_encoding="utf-8")
    if os.path.exists(".env")
    else Settings()
)
