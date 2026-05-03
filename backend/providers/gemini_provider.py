# type: ignore

import os

from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv('.env.development')


class GeminiProvider:
    def __init__(self):
        self.client = Client(api_key=os.getenv('GEMINI_API_KEY'))

    def generate_text(self, prompt: str, system_instruction: str, history: list[dict] | None = None) -> str:
        try:
            contents = self._build_contents(history or [], prompt)
            response = self.client.models.generate_content(
                model='gemini-3.1-flash-lite-preview',
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=system_instruction),
            )
            return response.text or 'Resposta vazia.'
        except Exception as e:
            raise RuntimeError(f'Falha no Gemini: {e}') from e

    def generate_embeddings(self, texts, batch_size=100):
        all_embeddings = []
        try:
            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]

                response = self.client.models.embed_content(
                    model='gemini-embedding-2-preview',
                    contents=batch,
                    config=types.EmbedContentConfig(output_dimensionality=1536, task_type='RETRIEVAL_DOCUMENT'),
                )

                if not response.embeddings:
                    raise ValueError('Nenhum vetor foi retornado para o lote de documentos.')

                batch_vectors = [emb.values for emb in response.embeddings]
                all_embeddings.extend(batch_vectors)

            return all_embeddings
        except Exception as e:
            raise RuntimeError(f'Falha ao gerar os vetores em lote: {e}') from e

    def _build_contents(self, history: list[dict], current_prompt: str) -> list[types.Content]:
        contents = []
        for message in history:
            contents.append(types.Content(role=message['role'], parts=[types.Part(text=message['content'])]))
        contents.append(types.Content(role='user', parts=[types.Part(text=current_prompt)]))
        return contents

    def generate_embedding(self, text, is_query=True):
        task_type = 'RETRIEVAL_QUERY' if is_query else 'RETRIEVAL_DOCUMENT'

        try:
            response = self.client.models.embed_content(
                model='gemini-embedding-2-preview',
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=1536, task_type=task_type),
            )

            if not response.embeddings or not response.embeddings[0].values:
                raise ValueError('Não foi possível gerar o vetor para esta consulta.')

            return response.embeddings[0].values
        except Exception as e:
            raise RuntimeError(f'Falha ao gerar o vetor ({task_type}): {e}') from e
