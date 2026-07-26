from pydantic_settings import BaseSettings
from typing import Optional 

class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: Optional[str] =None 
    database_username: Optional[str] =None
    database_name:str
    secret_key : str
    algorithm: str
    access_token_expire_mins: int

    class Config:
        env_file= ".env"
        extra = 'ignore'

settings = Settings()