from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env")

    api: ApiSettings = ApiSettings()
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    aws_region: str
    aws_bucket_name: str = "academease"
    presigned_url_expiration: int = 3600


@lru_cache
def get_settings():
    return Settings()
