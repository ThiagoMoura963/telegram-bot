# type: ignore
"""import io
import pytest
from backend.main import app

from backend.core.deps import get_current_user_id

@pytest.mark.parametrize(
    'file_name, content_type, content',
    [
        ('document.pdf', 'application/pdf', b'%PDF-1.4 fake pdf content'),
    ],
)
def test_upload_document(client, mocker, file_name, content_type, content):

    app.dependency_overrides[get_current_user_id] = lambda: 1

    mock_uuid = '550e8400-e29b-41d4-a716-446655440000'
    mock_chunks = [{'text': 'part 1', 'vector': [0.1]}]

    mocker.patch('backend.controllers.document_controller.get_document_processor')

    mock_doc_repo = mocker.patch('backend.controllers.document_controller.DocumentRepository').return_value
    mock_doc_repo.save.return_value = mock_uuid

    mock_chunks_repo = mocker.patch('backend.controllers.document_controller.ChunksRepository').return_value

    mock_service = mocker.patch('backend.controllers.document_controller.DocumentService').return_value
    mock_service.process.return_value = mock_chunks

    mock_file = (file_name, io.BytesIO(content), content_type)
    response = client.post('/api/v1/document/upload', files={'file': mock_file})

    app.dependency_overrides.clear()

    assert response.status_code == 200, f"Erro: {response.text}"

    data = response.json()
    assert 'id' in data, f"A chave 'id' não voltou no JSON. Voltou: {data}"
    assert data['id'] == mock_uuid
    assert data['file_name'] == file_name"""
