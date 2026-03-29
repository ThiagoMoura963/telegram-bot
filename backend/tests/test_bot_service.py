from unittest.mock import MagicMock, patch

from backend.services.bot_setup_service import BotSetupService


def test_register_webhook_success():
    service = BotSetupService()
    test_token = 'fake-token'
    test_url = 'http://test/webhook'

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            'ok': True,
            'description': 'Webhook configured',
        }

        success, message = service.register_webhook(test_token, test_url)

        assert success is True
        assert message == 'Webhook configured'

        expected_endpoint = f'https://api.telegram.org/bot{test_token}/setWebhook'

        mock_post.assert_called_once_with(
            expected_endpoint, data={'url': test_url}, timeout=10
        )


def test_get_telegram_info():
    service = BotSetupService()

    mock_response = MagicMock()
    mock_response.json.return_value = {
        'ok': True,
        'result': {'url': 'http://test/webhook', 'pending_update_count': 0},
    }

    with patch('requests.get', return_value=mock_response) as mock_get:
        info = service.get_telegram_info('fake-token')

        assert info['ok'] is True
        assert info['result']['url'] == 'http://test/webhook'

        expected_url = 'https://api.telegram.org/botfake-token/getWebhookInfo'
        mock_get.assert_called_once_with(expected_url)
