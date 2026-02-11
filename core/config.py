from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    secret_key: str
    algorithm: str
    refresh_token_expire_days: int
    access_token_expire_minutes: int

    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()
