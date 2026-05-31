from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #define your environment variables here as class attributes

    DATABASE_URL: str
    GEMINI_API_KEY: str
    JWT_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")

# Create an instance of the Settings class to load the environment variables
settings = Settings()