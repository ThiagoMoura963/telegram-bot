from dotenv import load_dotenv
import os 

load_dotenv()

REQUIRED_KEYS = ['GEMINI_API_KEY', 'TELEGRAM_API_KEY']
api_keys = {key: os.getenv(key) for key in REQUIRED_KEYS}
missing_keys = [key for key, value in api_keys.items() if value is None]

if missing_keys:
    raise ValueError(f'A(s) seguinte(s) chave(s) API não foi/foram encontrada(s) no .env {', '.join(missing_keys)}')

