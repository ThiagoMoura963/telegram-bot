from unittest.mock import patch


def test_post_telegram(client):
    api_token = 'at_token_de_teste'

    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 1,
            'date': 1711041600,
            'chat': {'id': 999, 'type': 'private'},
            'text': 'Hi, how are you?',
        },
    }

    target_telegram_provider = 'backend.controllers.telegram_controller.TelegramProvider'
    target_gemini_provider = 'backend.controllers.telegram_controller.GeminiProvider'
    target_chat_service = 'backend.controllers.telegram_controller.ChatService'
    target_repo = 'backend.controllers.telegram_controller.AgentRepository'
    with (
        patch(target_repo) as mock_repo_class,
        patch(target_telegram_provider) as mock_telegram,
        patch(target_gemini_provider),
        patch(target_chat_service) as mock_chat,
    ):
        mock_repo_class.return_value.get_by_api_token.return_value = {
            'id': 1,
            'user_id': 'uuid-teste',
            'api_token': api_token,
        }

        mock_chat.return_value.get_answer.return_value = 'Im fine'
        mock_telegram.return_value.process_webhook.return_value = None

        response = client.post(f'/api/v1/telegram/webhook/{api_token}', json=payload)

        assert response.status_code == 200
        assert response.json()['status'] == 'success'
