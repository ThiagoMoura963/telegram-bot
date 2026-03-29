from unittest.mock import patch


def test_post_telegram(client):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 1,
            'date': 1711041600,
            'chat': {'id': 999, 'type': 'private'},
            'text': 'Hi, how are you?',
        },
    }

    target_telegram_provider = (
        'backend.controllers.telegram_controller.TelegramProvider'
    )
    target_gemini_provider = 'backend.controllers.telegram_controller.GeminiProvider'
    target_chat_service = 'backend.controllers.telegram_controller.ChatService'

    with (
        patch(target_telegram_provider) as mock_telegram,
        patch(target_gemini_provider),
        patch(target_chat_service) as mock_chat,
    ):
        mock_chat.return_value.get_answer.return_value = 'Im fine'
        mock_telegram.return_value.process_webhook.return_value = None

        response = client.post('/api/v1/telegram/webhook', json=payload)

        assert response.status_code == 200
        assert response.json()['status'] == 'success'
