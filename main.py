from document_repository import DocumentRespository
from document_chunks_repository import DocumentChunksRepository
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from embedding_generator import EmbeddingGenerator
from chunk_generator import ChunksGenerator
import telegram_bot
import sys
import argparse

def process_file(file_path: str):
    print(f'Iniciando processamento do arquivo {file_path}')

    file_path = Path(file_path)

    if not file_path.is_file():
        print(f'Arquivo {file_path} não encontrado')
        sys.exit(1)

    file_name = file_path.name

    chunks_generator = ChunksGenerator()
    chunks_document = chunks_generator.extract_chunks(file_path)

    if chunks_document:
        chunks_text = [doc.page_content for doc in chunks_document]
        print(f'Arquivo dividido em {len(chunks_text)} chunks. Gerando embeddings...')

        embedding_generator = EmbeddingGenerator()
        embeddings = embedding_generator.generate_embeddings(chunks_text)
        print('Embeddings gerados. Salvando no banco de dados...')
        
        doc_repository = DocumentRespository()
        chunk_repo = DocumentChunksRepository()

        document_id = doc_repository.create(file_name)

        if not document_id:
            print('Falha ao criar o registro do documento.')
            sys.exit(1)   

        insert_data = []

        for i, (doc, embedding) in enumerate(zip(chunks_document, embeddings)):
            insert_data.append((doc.page_content, embedding, i))

        chunk_repo.bulk_insert(document_id, insert_data)

        print(f'\nDocumento "{file_name}" processado com sucesso.')
        print(f'{len(chunks_document)} chunks e seus vetores foram armazenados no banco de dados.')
    else:
        print(f'Não foi possível extrair os chunks do documento: {file_name}')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Aplicativo do Bot e Processador de Documentos.'
    )
    
    parser.add_argument(
        '--process-pdf',
        type=str,
        help='Caminho completo para o arquivo PDF que será processado e salvo no banco de dados.',
        metavar='FILE_PATH'
    )

    args = parser.parse_args()

    if args.process_pdf:
        process_file(args.process_pdf)
    else:
        print('Iniciando bot do Telegram...')
        telegram_bot.run()