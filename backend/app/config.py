from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    watsonx_api_key: Optional[str] = None
    watsonx_project_id: Optional[str] = None
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_model_id: str = "ibm/granite-13b-instruct-v2"
    database_url: str = "sqlite:///./thread.db"
    upload_dir: str = "./uploads"
    secret_key: str = "change-me-in-production"
    demo_mode: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
