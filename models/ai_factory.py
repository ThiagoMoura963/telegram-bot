from typing import Dict
import config
from .gemini_provider import GeminiProvider
from .ai_interface import AIProvider

def get_ai_client() -> AIProvider:
    PROVIDERS: Dict[str, type[AIProvider]] = {
        "GEMINI": GeminiProvider,
    }

    provider_class = PROVIDERS.get(str(config.AI_PROVIDER_TYPE), GeminiProvider)

    return provider_class()
