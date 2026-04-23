from fastapi import APIRouter, HTTPException, Request, status, Depends
from typing import Annotated

from backend.providers.gemini_provider import GeminiProvider
from backend.providers.telegram_provider import TelegramProvider
from backend.services.chat_service import ChatService
from backend.services.agent_setup_service import AgentSetupService
from backend.infra.repositories.agent_repository import AgentRepository
from backend.core.deps import get_current_user_id

router = APIRouter(prefix='/api/v1/telegram', tags=['Telegram Webhook'])

@router.post('/webhook/{api_token}')
async def telegram_webhook(api_token, request: Request):
    data = await request.json()

    agent_repository = AgentRepository()
    agent = agent_repository.get_by_api_token(api_token)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Agent not found.'
        )

    telegram_provider = TelegramProvider()
    chat_service = ChatService(provider=GeminiProvider())
    telegram_provider.process_webhook(agent['id'], agent['user_id'], data, chat_service)

    return {'status': 'success'}

@router.post('/activate')
def activate_agent(agent_id: str, token: str, request: Request, user_id: Annotated[str, Depends(get_current_user_id)]):
    base_url = str(request.base_url).rstrip('/')

    agent_repository = AgentRepository()
    agent = agent_repository.get_by_id(agent_id, user_id)

    if not agent:
        raise HTTPException(status_code=404, detail='Agent not found.')
    
    if not agent['is_active']:
        raise HTTPException(status_code=400, detail='Agent is disabled.')

    webhook_url = f'{base_url}/api/v1/telegram/webhook/{agent["api_token"]}'

    agent_setup_service = AgentSetupService(agent_repository)
    sucess, message = agent_setup_service.activate_agent(agent_id ,token, webhook_url, user_id)

    if not sucess:
        raise HTTPException(status_code=400, detail=message)

    return {'status': 'success', 'message': message, 'url': webhook_url}

@router.delete('/deactivate')
async def desactivate_agent(agent_id, token: str, user_id: Annotated[str, Depends(get_current_user_id)]):
    agent_setup_service = AgentSetupService(AgentRepository())

    success, message = agent_setup_service.deactivate_agent(agent_id, token, user_id)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {'status': 'success', 'message': message}

@router.get('/info/{token}')
def get_agent_info(token: str):
    agent_setup_service = AgentSetupService(AgentRepository())

    info = agent_setup_service.get_webhook_info(token)

    if not info.get('ok'):
        raise HTTPException(
            status_code=400, detail='Failed to retrieve agent information.'
        )

    return {'status': 'success', 'info': info.get('result')}
