import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    API_ID = int(os.getenv("API_ID", "25331263"))
    API_HASH = os.getenv("API_HASH", "cab85305bf85125a2ac053210bcd1030")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7977209272:AAEX0GrXV0hjWPJx6E_HLq-uOjAlqd7mul4")
    MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://rs92573993688:pVf4EeDuRi2o92ex@cluster0.9u29q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_URI = MONGO_URL
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "telegram_ai_bot")
    
    # AI
    AI_API_KEYS = json.loads(os.getenv("AI_API_KEYS", "{}"))
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
    
    # Admin
    OWNER_ID = int(os.getenv("OWNER_ID", "8043316865"))
    LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")
    if LOG_CHANNEL_ID:
        try:
            LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)
        except ValueError:
            LOG_CHANNEL_ID = None
    else:
        LOG_CHANNEL_ID = None
    
    # Force Subscribe Channel – safely handle non‑numeric values
    FORCE_SUBSCRIBE_CHANNEL = os.getenv("FORCE_SUBSCRIBE_CHANNEL")
    if FORCE_SUBSCRIBE_CHANNEL:
        try:
            FORCE_SUBSCRIBE_CHANNEL = int(FORCE_SUBSCRIBE_CHANNEL)
        except ValueError:
            FORCE_SUBSCRIBE_CHANNEL = None  # invalid, disable the feature
    else:
        FORCE_SUBSCRIBE_CHANNEL = None
    
    # Limits
    DAILY_FREE_LIMIT = int(os.getenv("DAILY_FREE_LIMIT", 100))
    PREMIUM_DAILY_LIMIT = int(os.getenv("PREMIUM_DAILY_LIMIT", 1000))
    
    # Server
    PORT = int(os.getenv("PORT", 8080))
    
    SUPPORTED_MODELS = {
        "gpt-3.5-turbo": "openai",
        "gpt-4": "openai",
        "gpt-4-turbo": "openai",
        "deepseek-chat": "deepseek",
        "gemini-pro": "gemini"
    }

config = Config()
