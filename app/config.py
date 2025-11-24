import os
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AI Studio Backend")

    # DB Credentials
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Auth Keys
    PASSWORD_KEY: str = os.getenv("PASSWORD_KEY")   # ← Your hashing key
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
