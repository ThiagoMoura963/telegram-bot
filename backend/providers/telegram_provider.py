import telebot
from telebot import types
from telegramify_markdown import markdownify

from backend.infra.repositories.agent_repository import AgentRepository
from backend.infra.repositories.chunks_repository import ChunksRepository
from backend.services.chat_service import ChatService


class TelegramProvider:
    def process_webhook(self, agent_id, user_id, json_data, chat_service: ChatService):
        agent_repository = AgentRepository()
        agent = agent_repository.get_by_id(agent_id, user_id)

        if not agent or not agent['is_active']:
            return

        print('ID do TELEGRAM:', agent['telegram_token'])

        bot = telebot.TeleBot(agent['telegram_token'])
        update = types.Update.de_json(json_data)

        if not (update and update.message and update.message.text):
            return

        chat_id = update.message.chat.id
        user_message = update.message.text

        embedding_message = chat_service.get_query_vector(user_message)

        chunk_repository = ChunksRepository()
        candidate_chunks = chunk_repository.find_similiar_chunk(embedding_message, limit=15, agent_id=agent_id)

        if candidate_chunks:
            context = '\n\n'.join(f'[Documento: {chunk["source"]}]\n{chunk["content"]}' for chunk in candidate_chunks)

            final_prompt = f"""
            Instrução: Use estritamente o contexto abaixo para responder 
            à pergunta do usuário.
            Se a resposta não estiver no contexto, diga que não sabe.

            Contexto:
            {context}

            Pergunta: 
            {user_message}
            """
        else:
            final_prompt = user_message

        answer = chat_service.get_answer(
            message=final_prompt,
            system_instruction=agent['system_prompt'],
        )

        formatted_answer = markdownify(answer)

        bot.send_message(chat_id, formatted_answer, parse_mode='MarkdownV2')
