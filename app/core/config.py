import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PORT: int = Field(8000, env="API_PORT")
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    DEBUG: bool = Field(True, env="DEBUG")
    
    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Firebase settings
    FIREBASE_PROJECT_ID: str = Field(..., env="FIREBASE_PROJECT_ID")
    FIREBASE_CLIENT_EMAIL: str = Field(..., env="FIREBASE_CLIENT_EMAIL")
    FIREBASE_PRIVATE_KEY: str = Field(..., env="FIREBASE_PRIVATE_KEY")
    
    # News API settings
    NEWSAPI_KEY: str = Field(..., env="NEWSAPI_KEY")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings() 