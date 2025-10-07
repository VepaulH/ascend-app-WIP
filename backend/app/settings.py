
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/wellness")
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    USE_PYTORCH: bool = os.getenv("USE_PYTORCH", "0") == "1"

settings = Settings()
