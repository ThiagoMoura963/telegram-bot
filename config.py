from dotenv import load_dotenv
import os

load_dotenv()

REQUIRED_KEYS = [
    'GEMINI_API_KEY', 
    'TELEGRAM_API_KEY', 
    'POSTGRES_USERNAME',
    'POSTGRES_PASSWORD',
    'POSTGRES_HOST',
    'POSTGRES_PORT',
    'POSTGRES_DATABASE'
]

_config_data = {key: os.getenv(key) for key in REQUIRED_KEYS}

missing_keys = [key for key, value in _config_data.items() if value is None]

if missing_keys:
    raise ValueError(f"As seguintes variáveis de ambiente não foram encontradas no .env: {', '.join(missing_keys)}")

GEMINI_API_KEY = _config_data['GEMINI_API_KEY']
TELEGRAM_API_KEY = _config_data['TELEGRAM_API_KEY']
POSTGRES_USERNAME = _config_data['POSTGRES_USERNAME']
POSTGRES_PASSWORD = _config_data['POSTGRES_PASSWORD']
POSTGRES_HOST = _config_data['POSTGRES_HOST']
POSTGRES_PORT = _config_data['POSTGRES_PORT']
POSTGRES_DATABASE = _config_data['POSTGRES_DATABASE']