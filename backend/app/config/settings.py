from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    debug: bool = True
    
    # JWT Configuration
    access_token_secret_key: str
    refresh_token_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int


    supabase_access_key_id: str = ""
    supabase_access_key_secret: str = ""
    supabase_endpoint: str = ""
    supabase_region: str = ""
    
    # Environment
    env: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

settings = Settings()