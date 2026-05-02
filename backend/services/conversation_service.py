from backend.infra.repositories.message_repository import MessageRepository

MAX_CONTEXT_MESSAGES = 20  # tamanho da janela deslizante


class ConversationService:
    def __init__(self):
        # Não precisa mais receber db como parâmetro!
        # O PostgresManager abre e fecha a conexão sozinho.
        self.repo = MessageRepository()

    def get_context(self, agent_id: str, chat_id: str) -> list[dict]:
        """Busca o histórico da conversa."""
        return self.repo.get_history(
            chat_id=chat_id,
            agent_id=agent_id,
            limit=MAX_CONTEXT_MESSAGES,
        )

    def add_message(self, agent_id: str, chat_id: str, role: str, content: str) -> None:
        """Salva uma mensagem no histórico."""
        self.repo.save(
            chat_id=chat_id,
            agent_id=agent_id,
            role=role,
            content=content,
        )

    def clear_context(self, agent_id: str, chat_id: str) -> None:
        """Apaga o histórico — usado no comando /reset."""
        self.repo.delete_history(chat_id=chat_id, agent_id=agent_id)
