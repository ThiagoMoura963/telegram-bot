from unittest.mock import patch, MagicMock

def test_post_telegram(client):
    payload = {
        'update_id': 12345,
        'message': {
            'message_id': 1,
            'date': 1711041600,
            'chat': {
                'id': 999, 
                'type': 'private'
            },
            'text': 'Hi, how are you?'
        }
    }

    telegram_target = 'telebot.TeleBot.send_message'
    service_target = 'backend.services.chat_service.ChatService.get_answer'
    with patch(telegram_target) as mock_send_message, \
        patch(service_target) as mock_service:

        mock_service.return_value = 'Im fine'

        response = client.post('/api/v1/telegram/webhook', json=payload)

        assert response.status_code == 200
        assert response.json()['status'] == 'success'

        mock_send_message.assert_called_once_with(999, 'Im fine')