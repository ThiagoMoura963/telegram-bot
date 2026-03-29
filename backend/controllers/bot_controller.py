from fastapi import APIRouter, HTTPException, Request

from backend.services.bot_setup_service import BotSetupService

router = APIRouter(prefix='/api/v1/bot', tags=['Bot Manager'])


@router.post('/activate')
def activate_bot(token: str, request: Request):
    base_url = str(request.base_url).rstrip('/')
    webhook_url = f'{base_url}/api/v1/telegram/webhook'

    bot_setup_service = BotSetupService()

    sucess, message = bot_setup_service.register_webhook(token, webhook_url)

    if not sucess:
        raise HTTPException(status_code=400, detail=message)

    return {'status': 'success', 'message': message, 'url': webhook_url}


@router.get('/info')
def get_bot_info(token: str):
    bot_setup_service = BotSetupService()

    info = bot_setup_service.get_telegram_info(token)

    if not info.get('ok'):
        raise HTTPException(
            status_code=400, detail='Failed to retrieve bot information.'
        )

    return {'status': 'success', 'info': info.get('result')}


@router.delete('/deactivate')
async def desactivate_bot(token: str):
    bot_setup_service = BotSetupService()

    success, message = bot_setup_service.delete_webook(token)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {'status': 'success', 'message': message}
