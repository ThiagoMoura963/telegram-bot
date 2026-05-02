from backend.processors.csv_processor import CsvProcessor
from backend.processors.pdf_processor import PdfProcessor
from backend.processors.xlsx_processor import XlsxProcessor

PROCESSORS_MAP = {
    'application/pdf': PdfProcessor,
    'text/csv': CsvProcessor,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': XlsxProcessor,
}


def get_document_processor(content_type):
    processor = PROCESSORS_MAP.get(content_type)

    if not processor:
        raise ValueError(f'O tipo {content_type} não é suportado.')

    return processor()
