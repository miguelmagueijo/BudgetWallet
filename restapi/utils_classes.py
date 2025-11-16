from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Budget Wallet REST API"
    version: str = "0.0.1"
    jwt_secret: str
    jwt_algorithm: str
    jwt_issuer: str
    db_url: str
    minutes_to_expire_token: int = 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=".env")