class ChatService:
    def __init__(self, provider):
        self.provider = provider

    def get_answer(self, message: str, system_instruction: str) -> str:
        response = self.provider.generate_text(
            prompt=self._build_prompt(message),
            system_instruction=system_instruction
        )

        if not response or not isinstance(response, str):
            raise ValueError("Resposta inválida do provider")

        response = response.strip()

        if not response:
            raise ValueError("Resposta vazia do provider")

        return response

    def _build_prompt(self, message: str) -> str:
        if not message:
            raise ValueError("Mensagem não pode ser vazia")

        return f"Pergunta:\n{message}"