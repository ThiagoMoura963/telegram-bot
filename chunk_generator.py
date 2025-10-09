import pypdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunksGenerator:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )

    def process_pdf(self, path):
        try:
            full_text = ''

            with open(path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                print(f'Lendo o arquivo...')
                for page in reader.pages:
                    full_text += page.extract_text() + '\n'

        except FileNotFoundError as e:
            print(f'Erro: O arquivo {path} não foi encontrado.')
            return None
        except Exception as e:
            print(f'Ocorreu um erro ao abrir o arquivo: {e}')
            return None
        
        if not full_text.strip():
            print('Nenhum texto foi extraído do PDF. Encerrando.') 
            return None
        
        return self.text_splitter.create_documents([full_text])