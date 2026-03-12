import numpy as np
from models.ai_factory import get_ai_client
from infra.repositories.document_chunks_repository import \
DocumentChunksRepository

class BotController:
    def __init__(self):
        self.ai = get_ai_client()
        self.repository: DocumentChunksRepository = DocumentChunksRepository()

    def get_answer(self, user_message: str) -> str:
        try:
            embedding_message = self.ai.get_embedding(user_message)

            if not embedding_message:
                return 'Não foi possível processar o sentido da sua mensagem' \
                ' no momento'

            query_vector = np.array(embedding_message)

            candidate_chunks = self.repository.find_similar_chunks(query_vector, limit=50)

            if not candidate_chunks:
                return 'Desculpe, não encontrei informações isso nos meus documentos.'
            
            context = '\n\n---\n\n'.join(candidate_chunks)

            final_prompt = f"""
            Instrução: Use estritamente o contexto abaixo para responder à pergunta do usuário.
            Se a resposta não estiver no contexto, diga que não sabe.

            Contexto:
            {context}

            Pergunta: 
            {user_message}
            """

            system_instruction = 'Você é um assistente técnico preciso e cordial.'
        
            return self.ai.send_message(final_prompt, system_instruction)
        except (ValueError, RuntimeError) as e:
            print("Erro:", e)
            return f'Ocorreu um erro no processamento {str(e)}'
        except Exception:
            return 'Erro interno no servidor. Por favor, tente novamente mais tarde'

