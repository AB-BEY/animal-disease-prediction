from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    
    DB_HOST: str = os.getenv("DB_HOST", "localhost")  # Default value if not found
    DB_USER: str = os.getenv("DB_USER", "root")       # Default value if not found
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))    # Convert to int
    DB_NAME: str = os.getenv("DB_NAME", "animal_diseases_prediction")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # Construct the DATABASE_URL
    DATABASE_URL: str = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Create an instance of Settings
settings = Settings()
