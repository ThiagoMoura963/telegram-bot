from pathlib import Path
from models.document_processor import DocumentProcessor
from models.ai_factory import get_ai_client
from infra.repositories.document_repository import DocumentRepository
from infra.repositories.document_chunks_repository import DocumentChunksRepository

class IngestionService:
    def __init__(self):
        self.ai = get_ai_client()
        self.processor = DocumentProcessor()
        self.doc_repo = DocumentRepository()
        self.chunk_repo = DocumentChunksRepository()

    def process_pdf(self, file_path_str: str):
        path = Path(file_path_str)
        if not path.is_file():
            raise FileNotFoundError(f'Arquivo não encontrado: {file_path_str}')

        chunks = self.processor.process_pdf(file_path_str)
        if not chunks:
            raise ValueError('Não foi possível extrair texto do PDF.')

        embeddings = self.ai.get_embeddings(chunks)

        doc_id = self.doc_repo.create(path.name)
        if not doc_id:
            raise RuntimeError("Falha ao criar registro do documento no banco.")

        insert_data = [
            (content, vector)
            for content, vector in zip(chunks, embeddings)
        ]

        self.chunk_repo.bulk_insert(doc_id, insert_data)
        return len(chunks)