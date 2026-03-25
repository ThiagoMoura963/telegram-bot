from unittest.mock import patch, MagicMock
from backend.services.bot_setup_service import BotSetupService


def test_activate_bot(client):
    target = 'backend.controllers.bot_controller.BotSetupService.register_webhook'

    with patch(target) as mock_setup:
        mock_setup.return_value = (True, 'Webhook set successfully')

        test_token = 'my-token'
        
        response = client.post(f'/api/v1/bot/activate?token={test_token}')

        assert response.status_code == 200

        data = response.json()
        assert data['status'] == 'success'

        expected_url = 'http://testserver/api/v1/telegram/webhook'
        assert data['url'] == expected_url

        mock_setup.assert_called_once_with(test_token, expected_url)


def test_get_bot_info(client):
    test_token = 'my-token'

    mock_telegram_response = {
        'ok': True,
        'result': {
            'url': 'http://testserver/api/v1/telegram/webhook',
            'pending_update_count': 0
        }
    }

    target = 'backend.controllers.bot_controller.BotSetupService.get_telegram_info'

    with patch(target) as mock_get_info:
        mock_get_info.return_value = mock_telegram_response
    
        response = client.get(f'/api/v1/bot/info?token={test_token}')

        assert response.status_code == 200

        data = response.json()
        assert data['status'] == 'success'
        assert data['info']['url'] == 'http://testserver/api/v1/telegram/webhook'

        mock_get_info.assert_called_once_with(test_token)
