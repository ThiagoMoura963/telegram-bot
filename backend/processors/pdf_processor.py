import io

from PyPDF2 import PdfReader


class PdfProcessor:
    def get_text(self, content):
        stream = io.BytesIO(content)
        reader = PdfReader(stream)

        full_text = ''
        for page in reader.pages:
            full_text += page.extract_text() + '\n'

        return full_text
