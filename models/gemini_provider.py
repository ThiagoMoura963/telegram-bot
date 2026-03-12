from google.genai import Client
from google.genai import types
from .ai_interface import AIProvider
from config import GEMINI_API_KEY

class GeminiProvider(AIProvider):
    def __init__(self):
        self.client: Client = Client(api_key=GEMINI_API_KEY)

    def send_message(self, prompt: str, system_instruction: str) -> str:
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )

        if not response.text:
            raise ValueError('Resposta vazia retornada pelo Gemini')

        return response.text
    
    def get_embedding(self, text: str) -> list[float]:
        try:
            result = self.client.models.embed_content(
                model='gemini-embedding-2-preview',
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=1536
                )
            )
            if not result.embeddings or not result.embeddings[0].values:
                raise ValueError("Falha ao gerar embedding.")
            return result.embeddings[0].values
        except Exception as e:
            raise RuntimeError(f"Erro no embedding: {e}")

    
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        try:                
            result = self.client.models.embed_content(
                model='gemini-embedding-2-preview',
                contents=list(texts),
                config=types.EmbedContentConfig(
                    output_dimensionality=1536
                )
            )

            if not result.embeddings:
                raise ValueError('Nenhum embedding retornado pelo Gemini')

                # O modelo suporta até 2048 textos por chamada
            return [e.values for e in result.embeddings if e.values is not None]
        except Exception as e:
            raise RuntimeError(f"Falha na vetorização em lote: {e}")