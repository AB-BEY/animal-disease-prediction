from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):

    DB_HOST: str = os.getenv("DB_HOST", "localhost")  # Default value if not found
    DB_USER: str = os.getenv("DB_USER", "root")       # Default value if not found
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))    # Convert to int
    DB_NAME: str = os.getenv("DB_NAME", "animal_diseases_prediction")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @property
    def DATABASE_URL(self):
        password = quote_plus(self.DB_PASSWORD)
        return (
            f"mysql+mysqlconnector://{self.DB_USER}:{password}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            "?charset=utf8mb4&ssl_ca=/etc/ssl/cert.pem"
        )

# Create an instance of Settings
settings = Settings()
