from enum import Enum
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings

class Environment(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"

class Settings(BaseSettings):
    ENVIRONMENT: str = Environment.LOCAL.value
    AWS_SECRET_ARN: str = "arn:aws:secretsmanager:us-west-1:059942430796:secret:ChiliMainSecret-6jF7ko"
    PG_LOCAL_DATABASE_URL: str
    ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env.local"
        case_sensitive = True
    

@lru_cache
def get_settings():
    return Settings()