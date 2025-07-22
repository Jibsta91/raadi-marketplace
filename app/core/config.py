from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Raadi Enterprise Marketplace"
    VERSION: str = "1.0.1"
    ENVIRONMENT: str = "development"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/raadi"
    
    # Redis settings
    REDIS_URL: str = "redis://redis:6379"
    
    # Elasticsearch settings
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    
    # Monitoring settings
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = True
    
    # AI services settings
    OPENAI_API_KEY: Optional[str] = None
    
    # AWS settings (for file uploads)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    
    # Email settings
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost", "http://localhost:3000"]
    
    # Norwegian marketplace categories
    MARKETPLACE_CATEGORIES = [
        "torget",
        "jobb",
        "bil-og-campingvogn",
        "eiendom",
        "reise",
        "bat",
        "mc",
        "nyttekjoretoy"
    ]
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()
