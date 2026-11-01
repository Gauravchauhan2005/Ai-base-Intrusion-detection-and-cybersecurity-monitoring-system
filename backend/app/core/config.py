from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Based Intrusion Detection & Cybersecurity Monitoring System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./ids_local.db"
    
    # Streaming backend ("redis", "kafka", or "memory")
    STREAM_BACKEND: str = "memory"
    REDIS_URL: str = "redis://localhost:6379/0"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    STREAM_TOPIC: str = "network_traffic_stream"
    CONSUMER_GROUP: str = "ids_inference_group"
    AUTO_START_CONSUMER: bool = True
    
    # ML & Artifacts
    MODEL_DIR: str = "ml/models"
    MODEL_VERSION: str = "v1.0.0"
    ANOMALY_THRESHOLD: float = 0.0
    ALERT_DEDUPLICATION_WINDOW_SEC: int = 5
    CRITICAL_CONFIDENCE_THRESHOLD: float = 0.85
    HIGH_CONFIDENCE_THRESHOLD: float = 0.70
    
    # Traffic Simulation Defaults
    DEFAULT_REPLAY_RATE_EPS: int = 25
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "*"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
