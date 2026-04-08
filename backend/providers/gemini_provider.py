import os
from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv('.env.development')

class GeminiProvider:
    def __init__(self):
        self.client = Client(api_key=os.getenv('GEMINI_API_KEY'))

    def generate_text(self, prompt: str, system_instruction: str) -> str:
        try:
            response = self.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
            )

            if not response.text:
                raise ValueError('O Gemini retornou uma resposta vazia')

            return response.text
        except Exception as e:
            raise RuntimeError(f'Falha na comunicação com o Gemini: {e}')

        
    def generate_embedding(self, text):
        try:
            response = self.client.models.embed_content(
                model='gemini-embedding-2-preview',
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=1536,
                    task_type='RETRIEVAL_QUERY'
                )
            )
    
            if not response.embeddings or not response.embeddings[0].values:
                raise ValueError('Não foi possível gerar o vetor para esta consulta.')
            
            return response.embeddings[0].values
        except Exception as e:
            raise RuntimeError(f'Falha ao gerar o vetor da consulta: {e}')
        
    def generate_embeddings(self, texts):
        try:
            response = self.client.models.embed_content(
                model='gemini-embedding-2-preview',
                contents=texts,
                config=types.EmbedContentConfig(
                    output_dimensionality=1536,
                    task_type='RETRIEVAL_DOCUMENT'
                )
            )

            if not response.embeddings:
                raise ValueError('Nenhum vetor foi retornado para o lote de documentos.')
            
            return [emb.values for emb in response.embeddings]
        except Exception as e:
            raise RuntimeError(f'Falha ao gerar os vetores dos documentos: {e}')