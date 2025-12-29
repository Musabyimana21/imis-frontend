from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./imis.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # MTN Mobile Money API
    MTN_MOMO_ENABLED: bool = False
    MTN_MOMO_ENVIRONMENT: str = "production"
    MTN_MOMO_BASE_URL: str = "https://momodeveloper.mtn.com"
    MTN_MOMO_SUBSCRIPTION_KEY: Optional[str] = None
    MTN_MOMO_API_USER: Optional[str] = None
    MTN_MOMO_API_KEY: Optional[str] = None
    MTN_MOMO_CALLBACK_URL: Optional[str] = None
    MTN_MOMO_CALLBACK_HOST: Optional[str] = None
    MTN_MOMO_TARGET_ENVIRONMENT: str = "mtnrwanda"
    MTN_MOMO_ACCOUNT: Optional[str] = None
    MTN_MOMO_MERCHANT_MSISDN: Optional[str] = None
    
    # Airtel Money API
    AIRTEL_MONEY_ENABLED: bool = False
    AIRTEL_MONEY_CLIENT_ID: Optional[str] = None
    AIRTEL_MONEY_CLIENT_SECRET: Optional[str] = None
    AIRTEL_MONEY_BASE_URL: str = "https://openapiuat.airtel.africa"
    
    # Payment Settings
    UNLOCK_FEE: float = 1000.0
    COMMISSION_RATE: float = 0.10
    PAYMENT_TIMEOUT_SECONDS: int = 300
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Email (Optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@imis.rw"
    
    # SMS (Optional)
    SMS_ENABLED: bool = False
    SMS_API_KEY: Optional[str] = None
    SMS_SENDER_ID: str = "IMIS"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
