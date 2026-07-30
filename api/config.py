from typing import Optional 
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


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    # class Config:
    #     env_file= ".env"
    #     extra = 'ignore'

settings = Settings()