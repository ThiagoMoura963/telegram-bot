# type: ignore

import os
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from backend.core.deps import get_current_user_id
from backend.services.agent_setup_service import AgentSetupService

from ..infra.repositories.agent_repository import AgentRepository

router = APIRouter(prefix='/api/v1/agent', tags=['Agent Manager'])


@router.get('')
def get_agents(user_id: Annotated[str, Depends(get_current_user_id)]):
    agent_repository = AgentRepository()
    agents = agent_repository.get_all(user_id)

    return {'agents': agents}


@router.post('')
async def create_agent(request: Request, user_id: Annotated[str, Depends(get_current_user_id)]):
    agent_repository = AgentRepository()

    try:
        agent_data = await request.json()
        agent_data['api_token'] = f'at_{secrets.token_urlsafe(32)}'

        agent_setup_service = AgentSetupService(agent_repository)

        is_valid, _ = agent_setup_service.validate_token(agent_data['telegram_token'])
        if not is_valid:
            raise HTTPException(
                status_code=400, detail={'field': 'tokenTelegram', 'message': 'Token inválido ou revogado.'}
            )

        new_agent = agent_repository.save(**agent_data, user_id=user_id)

        base_url = os.getenv('WEBHOOK_BASE_URL') or str(request.base_url).rstrip('/')
        webhook_url = f'{base_url}/api/v1/telegram/webhook/{agent_data["api_token"]}'
        print(f'DEBUG WEBHOOK URL: {webhook_url}')

        success, message = agent_setup_service.activate_agent(
            new_agent['id'], agent_data['telegram_token'], webhook_url, user_id
        )

        if not success:
            agent_repository.delete(new_agent['id'], user_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f'Falha ao ativar no Telegram: {message}'
            )

        return new_agent

    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        if 'new_agent' in locals() and new_agent:
            agent_repository.delete(new_agent['id'], user_id)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Erro interno ao processar a requisição.'
        ) from e


@router.put('/{agent_id}')
async def update_agent(agent_id, request: Request, user_id: Annotated[str, Depends(get_current_user_id)]):
    agent_data = await request.json()

    agent_repository = AgentRepository()
    setup_agent_service = AgentSetupService(agent_repository)

    old_agent = agent_repository.get_by_id(agent_id, user_id)
    if not old_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent not found.')

    new_token = agent_data.get('telegram_token')
    new_active_status = agent_data.get('is_active')

    token_changed = new_token and new_token != old_agent['telegram_token']
    status_changed = new_active_status is not None and new_active_status != old_agent['is_active']

    if token_changed:
        is_valid, _ = setup_agent_service.validate_token(new_token)
        if not is_valid:
            raise HTTPException(
                status_code=400, detail={'field': 'tokenTelegramConfig', 'message': 'Token inválido ou revogado.'}
            )

    base_url = str(request.base_url).rstrip('/')
    webhook_url = f'{base_url}/api/v1/telegram/webhook/{old_agent["api_token"]}'

    if token_changed:
        setup_agent_service.deactivate_agent(agent_id, old_agent['telegram_token'], user_id)

    final_active_status = new_active_status if new_active_status is not None else old_agent['is_active']
    token_to_use = new_token if new_token else old_agent['telegram_token']

    if final_active_status:
        if status_changed or token_changed:
            success, message = setup_agent_service.activate_agent(agent_id, token_to_use, webhook_url, user_id)
            if not success:
                raise HTTPException(status_code=400, detail=f'Erro ao ativar webhook no Telegram: {message}')
    else:
        if status_changed:
            setup_agent_service.deactivate_agent(agent_id, token_to_use, user_id)

    try:
        updated_agent = agent_repository.update(agent_id, agent_data, user_id)
    except Exception as e:
        print(f'Erro ao salvar agente: {str(e)}')
        raise HTTPException(status_code=500, detail='Erro interno ao processar a requisição.') from e

    return updated_agent


@router.delete('/{agent_id}')
async def delete_agent(agent_id, user_id: Annotated[str, Depends(get_current_user_id)]):
    agent_repository = AgentRepository()

    agent = agent_repository.get_by_id(agent_id, user_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent not found')

    agent_setup_service = AgentSetupService(agent_repository)

    agent_setup_service.deactivate_agent(agent_id, agent['telegram_token'], user_id)

    has_deleted = agent_repository.delete(agent_id, user_id)
    if not has_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agent not found.')

    return Response(status_code=status.HTTP_204_NO_CONTENT)
