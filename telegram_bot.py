import telebot
<<<<<<< HEAD
from config import api_keys
from call_gemini import send_message_to_gemini

bot = telebot.TeleBot(api_keys['TELEGRAM_API_KEY'])
=======
from config import TELEGRAM_API_KEY
from call_gemini import send_message_to_gemini

bot = telebot.TeleBot(TELEGRAM_API_KEY)
>>>>>>> 9876ff1 (Integrando Postgres com o Python através do pyscopg2)

@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    welcome_message = (
        'Olá! 👋 Sou um bot conectado ao Gemini.\n'
        'É só me enviar uma mensagem que eu te respondo.'
    )
    bot.reply_to(msg, welcome_message)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(msg: telebot.types.Message):
    user_message = msg.text

    thinking_message = bot.reply_to(msg, 'Aguarde...')

    gemini_response = send_message_to_gemini(user_message)

    bot.edit_message_text(
        text=gemini_response,
        chat_id=msg.chat.id,
        message_id=thinking_message.message_id
    )
def run():
    print('🤖 Bot em execução...')
    bot.infinity_polling()