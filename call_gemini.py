from google import genai
from google.genai import types
from config import GEMINI_API_KEY

SYSTEM_INSTRUCTION = """
    Você é um assistente de IA chamado 'Assistente de Documentos', especializado em analisar textos e responder perguntas de forma objetiva e factual.

    **Sua tarefa:**
    Responda à "Pergunta do Usuário" baseando-se única e exclusivamente nas informações contidas na seção "Contexto".

    **Regras estritas:**
    1.  **Tom e Estilo:** Seja sempre profissional, formal e direto. Não use gírias, opiniões pessoais, sarcasmo ou qualquer tipo de humor.
    2.  **Base na Fonte:** Cite a resposta diretamente do contexto sempre que possível. Não adicione informações que não estejam nos trechos fornecidos.
    3.  **Resposta Desconhecida:** Se a resposta para a pergunta não puder ser encontrada no "Contexto", responda EXATAMENTE com a frase: "Com base nos trechos analisados, não foi possível encontrar a resposta para esta pergunta." Não tente adivinhar ou inferir.
    """


def send_message_to_gemini(message: str) -> str:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
         
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )

        return response.text
    except Exception as e:
        print(f'Erro ao enviar mensagem para o Gemini: {e}')
        return 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.'


# def generate_embeddings(texts: list[str], task_type: str) -> list[list[float]]:
#     if not texts:
#         return []

#     try:
#         client = genai.Client(api_key=GEMINI_API_KEY)

#         for text in texts:
#             response = client.models.embed_content(
#                 model="models/embedding-001",
#                 contents=text,
#                 config=types.EmbedContentConfig(task_type=task_type)
#             )

#         embeddings = [e.values for e in response.embeddings]
#         return embeddings
    
#     except Exception as e:
#         print(f"Erro ao gerar embeddings em lote: {e}")
#         return []
