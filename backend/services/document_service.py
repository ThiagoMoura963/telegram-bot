from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.providers.gemini_provider import GeminiProvider
from backend.services.chat_service import ChatService


class DocumentService:
    def __init__(self, processor, chunk_size=1500, chunk_overlap=150):
        self.chat_service = ChatService(GeminiProvider())
        self.processor = processor
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )

    def process(self, content):
        try:
            text = self.processor.get_text(content)

            if not text.strip():
                raise ValueError(
                    'O documento está vazio ou não possui texto extraível.'
                )

            chunks = self.text_splitter.split_text(text)

            vectors = self.chat_service.get_document_vectors(chunks)

            return list(zip(chunks, vectors, strict=True))
        except Exception as e:
            raise Exception(f'Falha técnica ao processar o PDF: {e}') from e
