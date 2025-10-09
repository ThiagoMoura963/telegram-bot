import telebot
from config import TELEGRAM_API_KEY
from call_gemini import send_message_to_gemini
from embedding_generator import EmbeddingGenerator
import numpy as np
from document_chunks_repository import DocumentChunksRepository

bot = telebot.TeleBot(TELEGRAM_API_KEY)

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

    embedding_generator = EmbeddingGenerator()
    question_embedding  = embedding_generator.generate_embeddings([user_message])[0]
    question_embedding_np = np.array(question_embedding)

    chunk_repo = DocumentChunksRepository()
    relevant_chunks = chunk_repo.find_similar_chunks(question_embedding_np, 4)

    context = "\n\n---\n\n".join(relevant_chunks)
        
    final_prompt = f"""
        Você é um assistente especialista. Responda à pergunta do usuário baseando-se estritamente no contexto fornecido abaixo.
        Se a resposta não estiver clara no contexto, diga que a informação não foi encontrada nos trechos analisados.

        **Contexto:**
        ---
        {context}
        ---

        **Pergunta do Usuário:**
        {user_message}
        """
    
    print('Prompt final:', final_prompt)
    gemini_response = send_message_to_gemini(final_prompt)

    bot.edit_message_text(
        text=gemini_response,
        chat_id=msg.chat.id,
        message_id=thinking_message.message_id
    )

def run():
    print('🤖 Bot em execução...')
    bot.infinity_polling()