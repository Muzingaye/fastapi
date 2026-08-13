from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: Optional[str] =None 
    database_username: Optional[str] =None
    database_name:str
    secret_key : str
    algorithm: str
    access_token_expire_mins: int
    Debug: bool= False
    open_api_key: str
    allowed_origins: list[str]

    @field_validator("allowed_origins")
    @classmethod
    def parse_allowed_origins(cls, v)-> list[str]:
        if isinstance(v, str):
            return [o.strip() for o in v.split(',')]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive= False,
    )
settings = Settings()