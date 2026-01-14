import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size=1500, chunk_overlap=150):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def process_pdf(self, path: str) -> list[str]:
        try:
            full_text = ''
            with open(path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + '\n'

            if not full_text.strip():
                raise ValueError("O PDF está vazio ou não possui texto extraível.")
            
            chunks = self.text_splitter.split_text(full_text)
            return chunks
        
        except Exception as e:
            raise RuntimeError(f"Falha técnica ao processar o PDF: {e}")