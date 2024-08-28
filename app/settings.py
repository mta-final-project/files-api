from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8003


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    aws_bucket_name: str = "academease-materials"
    presigned_url_expiration: int = 3600


@lru_cache
def get_settings():
    return Settings()
