from fastapi import APIRouter, Request
from backend.providers.telegram_provider import TelegramProvider
from backend.providers.gemini_provider import GeminiProvider
from backend.services.chat_service import ChatService

router = APIRouter(prefix='/api/v1/telegram', tags=['Telegram Webhook'])

@router.post('/webhook')
async def telegram_webhook(request: Request):
    data = await request.json()

    telegram_provider = TelegramProvider()
    chat_service = ChatService(provider=GeminiProvider())
    telegram_provider.process_webhook(data, chat_service)

    return {'status': 'success'}
