import numpy as np
from document_repository import DocumentRespository
from document_chunks_repository import DocumentChunksRepository
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from embedding_generator import EmbeddingGenerator
from chunk_generator import ChunksGenerator
# from call_gemini import generate_embeddings, send_message_to_gemini
import telegram_bot

if __name__ == '__main__':
    telegram_bot.run()
    # full_text = ''
    # folder_name = 'books'
    # file_name = 'Pai Rico, Pai Pobre - Robert T. Kiyosaki.pdf'

    # pdf_path = Path(__file__).parent / folder_name / file_name

    # chunks_generator = ChunksGenerator()
    # chunks_document = chunks_generator.process_pdf(pdf_path)

    # if chunks_document:
    #     chunks_text = [doc.page_content for doc in chunks_document]

    #     embedding_generator = EmbeddingGenerator()
    #     embeddings = embedding_generator.generate_embeddings(chunks_text)
        
    #     doc_repository = DocumentRespository()
    #     chunk_repo = DocumentChunksRepository()

    #     document_id = doc_repository.create(file_name)

    #     if not document_id:
    #         print('Falha ao criar o registro do documento')
    #         exit(1)   

    #     insert_data = []

    #     for i, (doc, embedding) in enumerate(zip(chunks_document, embeddings)):
    #         insert_data.append((doc.page_content, embedding, i))

    #     chunk_repo.bulk_insert(document_id, insert_data)

    #     print(f'\nDocumento "{file_name}" processado com sucesso.')
    #     print(f'{len(chunks_document)} chunks e seus vetores foram armazenados no banco de dados.')