from google import genai
from google.genai import types
from config import GEMINI_API_KEY
def send_message_to_gemini(message: str) -> str:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction='Responda de forma agressiva e debochada'
            )
        )

        return response.text
    except Exception as e:
        print(f'Erro ao enviar mensagem para o Gemini: {e}')
        return 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.'