import secrets
from typing import Any, Dict, List, Optional, Union 

from pydantic.v1 import AnyHttpUrl, BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Token settings
    ALGORITHM: str = "HS256"
    ACESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    FRONTEND_HOST: str =  "localhost"
    FRONTEND_PORT: int = 3000

    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "freela_facility"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # External Server URLs
    FILE_PROCESSOR_URL: str = "http://localhost: 5000"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v 
        return PostgresDsn.build(
            schema="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get("POSTGRES_DB") or ''}",
        )

    # File upload settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100 MB

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
    
