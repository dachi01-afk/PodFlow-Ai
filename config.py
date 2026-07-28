from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # ElevenLabs
    elevenlabs_api_key: str
    
    # Qwen (via Groq)
    qwen_api_key: str
    qwen_api_url: str = "https://api.groq.com/openai/v1"
    
    # Agnes AI
    agnes_api_key: str
    agnes_api_url: str = "https://apihub.agnes-ai.com/v1"
    
    # Redis (untuk Celery)
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
