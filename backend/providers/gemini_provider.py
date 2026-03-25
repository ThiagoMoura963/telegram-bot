from google.genai import Client, types
from dotenv import load_dotenv
import os

load_dotenv('.env.development')

class GeminiProvider:
    def __init__(self):
        self.client = Client(api_key=os.getenv('GEMINI_API_KEY'))

    def generate_text(self, prompt: str, system_instruction: str) -> str:
        try:   
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )    

            if not response.text:
                raise ValueError('Resposta vazia do Gemini')

            return response.text
        except Exception as e:
            print(f'MENSAGEM DO ERRO: {str(e)}')
            raise RuntimeError('Erro no provedor Gemini')
        