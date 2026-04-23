from unittest.mock import patch, ANY
from backend.main import app
from backend.core.deps import get_current_user_id

def test_activate_bot(client):
    app.dependency_overrides[get_current_user_id] = lambda: "user-id-teste"
    
    repo_target = 'backend.controllers.telegram_controller.AgentRepository'
    service_target = 'backend.controllers.telegram_controller.AgentSetupService.activate_agent'
    
    with patch(repo_target) as mock_repo_class, \
         patch(service_target) as mock_setup:
        
        mock_repo_instance = mock_repo_class.return_value
        
        mock_repo_instance.get_by_id.return_value = {
            'id': 1, 
            'name': 'Agente Teste',
            'telegram_token': 'my-token',
            'api_token': 'at_token_teste_123',
            'user_id': 'user-id-teste',
            'is_active': True
        }
        
        mock_setup.return_value = (True, 'Webhook set successfully')
        
        test_token = 'my-token'
        agent_id = 1

        response = client.post(f'/api/v1/telegram/activate?agent_id={agent_id}&token={test_token}')

        app.dependency_overrides = {}

        assert response.status_code == 200
        assert response.json()['status'] == 'success'

def test_get_bot_info(client):
    test_token = 'my-token'
    
    mock_telegram_response = {
        'ok': True,
        'result': {
            'url': 'http://testserver/api/v1/telegram/webhook',
            'pending_update_count': 0,
        },
    }

    target = 'backend.controllers.telegram_controller.AgentSetupService.get_webhook_info'

    with patch(target) as mock_get_info:
        mock_get_info.return_value = mock_telegram_response

        response = client.get(f'/api/v1/telegram/info/{test_token}')

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert data['info']['url'] == 'http://testserver/api/v1/telegram/webhook'