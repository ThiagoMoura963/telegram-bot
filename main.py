# from telegram_bot import run
from document_repository import DocumentRespository
from document_chunks_repository import DocumentChunksRepository
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf
from pathlib import Path
from embedding_generator import EmbeddingGenerator
# from call_gemini import generate_embeddings, send_message_to_gemini

if __name__ == '__main__':
    embedding_generator = EmbeddingGenerator()
    
    full_text = ''
    folder_name = 'books'
    file_name = 'Pai Rico, Pai Pobre - Robert T. Kiyosaki.pdf'

    pdf_path = Path(__file__).parent / folder_name / file_name

    try:
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            print(f'Lendo o arquivo "{file_name}"...')
            for page in reader.pages:
                full_text += page.extract_text() + '\n'

    except FileNotFoundError as e:
        print(f'Erro: O arquivo {pdf_path} não foi encontrado.')
        exit(1)
    except Exception as e:
        print(f'Ocorreu um erro ao abrir o arquivo: {e}')
        exit(1)

    if not full_text.strip():
        print('Nenhum texto foi extraído do PDF. Encerrando.')
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,      
            length_function=len,
            is_separator_regex=False
        )

        chunks_documents = text_splitter.create_documents([full_text])
        print(f'Documento dividido em {len(chunks_documents)} chunks.')

        chunk_text = [doc.page_content for doc in chunks_documents]

        embeddings = embedding_generator.generate_embeddings(chunk_text)

        doc_repository = DocumentRespository()
        chunk_repo = DocumentChunksRepository()

        document_id = doc_repository.create(file_name)

        if not document_id:
            print('Falha ao criar o registro do documento')
            exit(1)   

        insert_data = []

        for i, (doc, embedding) in enumerate(zip(chunks_documents, embeddings)):
            insert_data.append((doc.page_content, embedding, i))

        chunk_repo.bulk_insert(document_id, insert_data)

        print(f'\nDocumento "{file_name}" processado com sucesso.')
        print(f'{len(chunks_documents)} chunks e seus vetores foram armazenados no banco de dados.')