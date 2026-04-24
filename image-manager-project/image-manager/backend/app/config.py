from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./images.db"
    STORAGE_TYPE: str = "local"
    OSS_ENDPOINT: str = ""
    OSS_BUCKET: str = ""
    OSS_ACCESS_KEY: str = ""
    OSS_SECRET_KEY: str = ""
    OSS_CDN_DOMAIN: str = ""

    class Config:
        env_file = ".env"

settings = Settings()