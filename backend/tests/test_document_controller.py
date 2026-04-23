# type: ignore
import io

import pytest

from backend.infra.repositories.chunks_repository import ChunksRepository
from backend.infra.repositories.document_resository import DocumentRepository
from backend.services.document_service import DocumentService


@pytest.mark.parametrize(
    'file_name, content_type, content',
    [
        ('document.pdf', 'application/pdf', b'%PDF-1.4 fake pdf content'),
        # ('data.csv', 'text/csv', b'id,name\n1,John'),
    ],
)
def test_upload_document(client, mocker, file_name, content_type, content):
    mock_uuid = '550e8400-e29b-41d4-a716-446655440000'
    mock_chunks = [{'text': 'part 1', 'vector': [0.1]}]

    mock_doc_repo_class = mocker.patch('backend.controllers.document_controller.DocumentRepository', autospec=True)
    mock_doc_repo: DocumentRepository = mock_doc_repo_class.return_value
    mock_doc_repo.save.return_value = mock_uuid

    mock_chunks_repo_class = mocker.patch('backend.controllers.document_controller.ChunksRepository', autospec=True)
    mock_chunks_repo: ChunksRepository = mock_chunks_repo_class.return_value

    mock_get_processor = mocker.patch('backend.controllers.document_controller.get_document_processor')

    mock_service_class = mocker.patch('backend.controllers.document_controller.DocumentService', autospec=True)
    mock_service: DocumentService = mock_service_class.return_value
    mock_service.process.return_value = mock_chunks

    mock_file = (file_name, io.BytesIO(content), content_type)

    response = client.post('/api/v1/document/upload', files={'file': mock_file})

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == mock_uuid
    assert data['file_name'] == file_name

    mock_get_processor.assert_called_with(content_type)
    mock_service.process.assert_called_once_with(content)
    mock_doc_repo.save.assert_called_once_with(file_name)
    mock_chunks_repo.save_all.assert_called_once_with(mock_uuid, mock_chunks)
