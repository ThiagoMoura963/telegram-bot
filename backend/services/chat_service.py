class ChatService:
    def __init__(self, provider):
        self.provider = provider

    def get_answer(
        self,
        message,
        system_instruction,
        history: list[dict] | None = None,
    ):
        try:
            return self.provider.generate_text(prompt=message, system_instruction=system_instruction, history=history)
        except Exception as e:
            raise RuntimeError(f'ChatService falhou ao gerar resposta: {e}') from e

    def get_query_vector(self, text, is_query=True):
        try:
            return self.provider.generate_embedding(text, is_query=is_query)
        except Exception as e:
            raise RuntimeError(f'ChatService falhou ao vetorizar consulta: {e}') from e

    def get_document_vectors(self, texts):
        try:
            return self.provider.generate_embeddings(texts)
        except Exception as e:
            raise RuntimeError(f'ChatService falhou ao vetorizar documentos: {e}') from e
