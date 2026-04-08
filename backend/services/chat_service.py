class ChatService:
    def __init__(self, provider):
        self.provider = provider

    def get_answer(self, message, system_instruction):
        try:
            return self.provider.generate_text(message, system_instruction)
        except Exception as e:
            raise RuntimeError(f'ChatService falhou ao gerar resposta: {e}')

    def get_query_vector(self, text):
        try:
            return self.provider.generate_embedding(text)
        except Exception as e:
            raise RuntimeError(f'ChatService falhou ao vetorizar consulta: {e}')

    def get_document_vectors(self, texts):
        try:
            return self.provider.generate_embeddings(texts)
        except Exception as e:
            raise RuntimeError(f'ChatService falhou ao vetorizar documentos: {e}')