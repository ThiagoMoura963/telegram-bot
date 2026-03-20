from unittest.mock import patch, MagicMock

def test_post_chat(client):
    target = 'backend.controllers.chat_controller.GeminiProvider'

    with patch(target) as MockProvider:
        mock_instance = MockProvider.return_value
        mock_instance.generate_text.return_value = 'Im fine'

        payload = {
            'message': 'Hi, how are you?',
            'api_key': 'dummy-key',
            'system_instruction': 'Be an assistant'
        }
        
        response = client.post('/api/v1/chat', json=payload)

        assert response.status_code == 200
        assert response.json()['answer'] == 'Im fine'

        mock_instance.generate_text.assert_called_once_with(
            prompt='Pergunta:\nHi, how are you?',
            system_instruction='Be an assistant'
        )
