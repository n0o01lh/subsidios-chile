from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://localhost/subsidios_chile'
    redis_url: str = 'redis://localhost:6379/0'
    backend_cors_origins: list[str] = ['http://localhost:5173']

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings = Settings()
