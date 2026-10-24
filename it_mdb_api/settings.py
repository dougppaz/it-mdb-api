from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")
    name: str = "it-mdb-api"
    env: str = "development"
    debug: bool = True


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    redis_url: str = "redis://localhost:6379/0"
    queue_redis_url: str = "redis://localhost:6379/1"
    use_fake_redis: bool = False


class TmdbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    tmdb_api_read_access_token: str = ""


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    tmdb: TmdbSettings = TmdbSettings()


settings = Settings()
