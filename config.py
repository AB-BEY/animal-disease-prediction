from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str

    # Reset token
    RESET_TOKEN_EXPIRE_MINUTES: int = 30
    RESET_TOKEN_SECRET: str

    DB_HOST: str = os.getenv("DB_HOST")  # Default value if not found
    DB_USER: str = os.getenv("DB_USER")      # Default value if not found
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))    # Convert to int
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    # Construct the DATABASE_URL
    DATABASE_URL: str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Create an instance of Settings
settings = Settings()
