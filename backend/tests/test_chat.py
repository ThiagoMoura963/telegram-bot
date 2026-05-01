# # type: ignore
# from backend.services.chat_service import ChatService


# def test_post_chat(mocker):
#     target = 'backend.providers.gemini_provider.GeminiProvider'
#     mock_provider = mocker.patch(target).return_value
#     mock_provider.generate_text.return_value = 'Im fine'

#     service = ChatService(provider=mock_provider)

#     system_instruction = 'Be an assistant'
#     user_text = 'Hi, how are you?'

#     answer = service.get_answer(user_text, system_instruction)

#     assert answer == 'Im fine'

#     mock_provider.generate_text.assert_called_once_with(user_text, system_instruction)
