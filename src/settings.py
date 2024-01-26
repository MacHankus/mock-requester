import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PORT: int = 8080

    CONFIG_FILE_PATH: str = 'config.yaml'

settings = (
    Settings(_env_file=".env", _env_file_encoding="utf-8")
    if os.path.exists(".env")
    else Settings()
)
