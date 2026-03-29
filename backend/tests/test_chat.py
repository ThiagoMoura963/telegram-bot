from unittest.mock import patch

from backend.services.chat_service import ChatService


def test_post_chat():
    provider_target = 'backend.providers.gemini_provider.GeminiProvider'

    with patch(provider_target) as MockProvider:
        mock_instance = MockProvider.return_value
        mock_instance.generate_text.return_value = 'Im fine'

        service = ChatService(provider=mock_instance)

        system_instruction = 'Be an assistant'
        user_text = 'Hi, how are you?'

        answer = service.get_answer(user_text, system_instruction)

        assert answer == 'Im fine'

        mock_instance.generate_text.assert_called_once_with(
            prompt='Pergunta:\nHi, how are you?', system_instruction=system_instruction
        )
