#type: ignore

from unittest.mock import MagicMock, patch
from backend.services.agent_setup_service import AgentSetupService

def test_register_webhook_success():
    mock_repo = MagicMock()
    service = AgentSetupService(mock_repo)
    
    test_token = 'fake-token'
    test_url = 'http://test/webhook'
    user_id = 'user-id-teste'

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            'ok': True,
            'description': 'Webhook configured',
        }

        success, message = service.activate_agent(1, test_token, test_url, user_id)
        
        assert success is True
        assert message == 'Webhook configured'

        expected_endpoint = f'https://api.telegram.org/bot{test_token}/setWebhook'
        
        mock_post.assert_called_once_with(
            expected_endpoint, 
            data={'url': test_url},
            timeout=10
        )

def test_get_telegram_info():
    mock_repo = MagicMock()
    service = AgentSetupService(mock_repo)

    mock_response = MagicMock()
    mock_response.json.return_value = {
        'ok': True,
        'result': {'url': 'http://test/webhook', 'pending_update_count': 0},
    }

    with patch('requests.get', return_value=mock_response) as mock_get:
        info = service.get_webhook_info('fake-token')

        assert info['ok'] is True
        assert info['result']['url'] == 'http://test/webhook'

        expected_url = 'https://api.telegram.org/botfake-token/getWebhookInfo'
        mock_get.assert_called_once_with(expected_url, timeout=10)