from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BhuDrishti AI"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./bhudrishti.db"
    weather_api_base_url: str = "https://api.open-meteo.com/v1"

    satellite_stac_url: str = "https://stac.dataspace.copernicus.eu/v1/"
    satellite_default_cloud_cover_max: float = 40.0
    satellite_search_days: int = 30

    cdse_username: str | None = None
    cdse_password: str | None = None

    cdse_s3_endpoint: str = "https://eodata.dataspace.copernicus.eu"
    cdse_s3_region: str = "default"
    cdse_access_key: str | None = None
    cdse_secret_key: str | None = None

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
