from backend.processors.pdf_processor import PdfProcessor

PROCESSORS_MAP = {'application/pdf': PdfProcessor}


def get_document_processor(content_type):
    processor = PROCESSORS_MAP.get(content_type)

    if not processor:
        raise ValueError(f'O tipo {content_type} não é suportado.')

    return processor()
