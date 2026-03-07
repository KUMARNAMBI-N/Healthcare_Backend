from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Healthcare API"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "changeme_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost:5432/doctor-service"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Razorpay
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
