# type: ignore
import os

import telebot
from dotenv import load_dotenv
from telebot import types

from backend.services.chat_service import ChatService

load_dotenv('.env.development')


class TelegramProvider:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_API_KEY')
        self.bot = telebot.TeleBot(self.token)

    def process_webhook(self, json_data, chat_service: ChatService):
        update = types.Update.de_json(json_data)

        if update and update.message and update.message.text:
            chat_id = update.message.chat.id
            user_text = update.message.text

            answer = chat_service.get_answer(
                message=user_text,
                system_instruction='Você é um assistente engraçado, sempre quer '
                'fazer uma piada para desdescontrair.',
            )

            self.bot.send_message(chat_id, answer)
