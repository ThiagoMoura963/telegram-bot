# from telegram_bot import run
from document_repository import DocumentRespository

if __name__ == '__main__':
    # run()
    doc_repository = DocumentRespository()
    file_name = 'Meu Arquivo PDF'
    doc_repository.create(file_name)