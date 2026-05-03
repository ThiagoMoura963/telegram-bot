# type: ignore

import telebot
from telebot import types
from telegramify_markdown import markdownify

from backend.infra.repositories.agent_repository import AgentRepository
from backend.infra.repositories.chunks_repository import ChunksRepository
from backend.infra.repositories.message_repository import MessageRepository
from backend.services.conversation_service import ConversationService


class TelegramProvider:
    def __init__(self):
        self.agent_repo = AgentRepository()
        self.message_repo = MessageRepository()

    def process_webhook(self, agent_id, user_id, json_data, chat_service):
        agent = self.agent_repo.get_by_id(agent_id, user_id)
        if not agent or not agent['is_active']:
            return

        bot = telebot.TeleBot(agent['telegram_token'])
        update = types.Update.de_json(json_data)

        conv_service = ConversationService(self.message_repo, ChunksRepository(), chat_service)

        self._register_handlers(bot, agent_id, user_id, chat_service, conv_service, agent)

        bot.process_new_updates([update])

    def _register_handlers(self, bot, agent_id, user_id, chat_service, conv_service, agent):
        @bot.message_handler(commands=['reset'])
        def handle_reset(message):
            self.message_repo.delete_history(user_id=user_id, agent_id=agent_id)
            bot.send_message(message.chat.id, '🔄 Histórico apagado!')

        @bot.message_handler(commands=['registrar'])
        def handle_register(message):
            content = telebot.util.extract_arguments(message.text)
            if not content:
                bot.send_message(message.chat.id, '⚠️ Uso: `/registrar seu texto`')
                return

            vector = chat_service.get_query_vector(content, is_query=False)
            self.message_repo.save(user_id, agent_id, 'user', content, vector)
            bot.send_message(message.chat.id, '✅ Registrado!')

        @bot.message_handler(func=lambda message: True)
        def handle_chat(message):
            feedback_msg = bot.send_message(message.chat.id, '_Processando..._', parse_mode='Markdown')

            try:
                bot.send_chat_action(message.chat.id, 'typing')

                answer = conv_service.execute_chat_flow(
                    user_id=user_id, agent_id=agent_id, text=message.text, system_prompt=agent['system_prompt']
                )

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=feedback_msg.message_id,
                    text=markdownify(answer),
                    parse_mode='MarkdownV2',
                )

            except Exception as e:
                print(f'ERRO NO FLUXO DE CHAT: {e}')
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=feedback_msg.message_id,
                    text='❌ Ops, ocorreu um erro ao processar sua resposta.',
                )
