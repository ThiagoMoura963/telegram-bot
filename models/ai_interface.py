from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def send_message(self, prompt:str, system_instruction: str) -> str: ...

    @abstractmethod
    def get_embedding(self, text: str) -> list[str]: ...

    @abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]: ...  