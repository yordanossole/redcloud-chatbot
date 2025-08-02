import os
from dotenv import load_dotenv

load_dotenv()

SESSION_EXPIRY_MINUTES = int(os.getenv("SESSION_EXPIRY_MINUTES", 30))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", " ")
GEMINI_API_MODEL = os.getenv("GEMINI_API_MODEL", " ")