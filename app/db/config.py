import os

# from pydantic import Field
# from pydantic_settings import BaseSettings
from pydantic import BaseSettings, Field



class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')

settings = Settings()