# type: ignore
import os

import telebot
from dotenv import load_dotenv
from telebot import types

from backend.infra.repositories.chunks_repository import ChunksRepository
from backend.services.chat_service import ChatService

load_dotenv('.env.development')


class TelegramProvider:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_API_KEY')
        self.bot = telebot.TeleBot(self.token)

    def process_webhook(self, json_data, chat_service: ChatService):
        update = types.Update.de_json(json_data)

        if not (update and update.message and update.message.text):
            return

        chat_id = update.message.chat.id
        user_message = update.message.text

        embedding_message = chat_service.get_query_vector(user_message)

        chunk_repository = ChunksRepository()
        candidate_chunks = chunk_repository.find_similiar_chunk(embedding_message, 15)

        if candidate_chunks:
            context = '\n\n'.join(
                f'[Documento: {chunk["source"]}]\n{chunk["content"]}'
                for chunk in candidate_chunks
            )

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
            system_instruction='Responda de forma ignorante',
        )

        self.bot.send_message(chat_id, answer)
