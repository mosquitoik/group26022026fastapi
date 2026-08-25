from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str
    MONGO_BOOK_COLLECTION: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Keeps the app from crashing if there are extra variables in your .env
    )



settings = Settings()