import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/students")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    TWILIO_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_FROM: str = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

settings = Settings()
