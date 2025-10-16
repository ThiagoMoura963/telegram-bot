import telebot
import torch
from config import TELEGRAM_API_KEY
from call_gemini import send_message_to_gemini
from embedding_generator import EmbeddingGenerator
import numpy as np
from document_chunks_repository import DocumentChunksRepository
from sentence_transformers import CrossEncoder

bot = telebot.TeleBot(TELEGRAM_API_KEY)
embedding_generator = EmbeddingGenerator()
cross_encoder = CrossEncoder('BAAI/bge-reranker-base', device='cuda' if torch.cuda.is_available() else 'cpu')

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

    print('Etapa 1: Recuperando chunks com Bi-Encoder...')


    question_embedding  = embedding_generator.generate_embeddings([user_message])[0]
    question_embedding_np = np.array(question_embedding)

    chunk_repo = DocumentChunksRepository()
    candidate_chunks = chunk_repo.find_similar_chunks(question_embedding_np, 50)

    if not candidate_chunks:
        bot.edit_message_text(
            'Não encontrei a informação sobre isso',
            chat_id=msg.chat.id,
            message_id=thinking_message.message_id
        )
        return

    print(f'Etapa 2: Reclassificando {len(candidate_chunks)} chunks com Cross-Encoder...')

    sentence_pair = [[user_message, chunk] for chunk in candidate_chunks]

    scores = cross_encoder.predict(sentence_pair, show_progress_bar=True)
    scored_chunks = list(zip(scores, candidate_chunks))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    reranked_chunks = [chunk for score, chunk in scored_chunks[:20]]

    print('Etapa 3: Gerando resposta com base nos chunks reclassificados.')
        
    context = "\n\n---\n\n".join(reranked_chunks)

    final_prompt = f"""
    ---
    **Contexto:**
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