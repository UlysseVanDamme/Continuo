import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    INGEST_API_KEY: str = os.getenv("INGEST_API_KEY")
    WEBSITE_LINK: str = os.getenv("WEBSITE_LINK")

settings = Settings()