#type: ignore

import telebot
from telebot import types 
from config import TELEGRAM_API_KEY
from controller.bot_controller import BotController

if not TELEGRAM_API_KEY:
    raise ValueError("TELEGRAM_API_KEY não encontrada no arquivo .env")

bot = telebot.TeleBot(TELEGRAM_API_KEY)
controller = BotController()

@bot.message_handler(func=lambda message: True)
def handle_all_messages(msg: types.Message):
    if not msg.text:
        bot.reply_to(msg, "No momento, eu só consigo processar perguntas em texto.")
        return
    
    status_msg = bot.reply_to(msg, 'Consultando documentos e gerando resposta...')

    try:
        answer = controller.get_answer(msg.text)

        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=status_msg.message_id,
            text=answer,
            parse_mode='Markdown' 
        )

    except Exception as e:
        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=status_msg.message_id,
            text="Tive um problema ao formatar a resposta. Tente novamente."
        )

def run():
    print('Bot iniciado...')
    bot.infinity_polling()
    