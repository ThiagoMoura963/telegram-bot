from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from backend.core.deps import get_current_user_id
from backend.infra.repositories.chunks_repository import ChunksRepository
from backend.infra.repositories.document_resository import DocumentRepository
from backend.processors.factory import get_document_processor
from backend.services.document_service import DocumentService

router = APIRouter(prefix='/api/v1/document', tags=['Document Manager'])


@router.get('/{agent_id}')
async def get_document(user_id: Annotated[str, Depends(get_current_user_id)], agent_id):

    document_repository = DocumentRepository()
    documents = document_repository.get_all(user_id, agent_id)

    return {'documents': documents}


@router.post('/upload')
async def upload_document(file: Annotated[UploadFile, File()]):
    content = await file.read()

    document_processor = get_document_processor(file.content_type)
    document_service = DocumentService(document_processor)
    chunks_data = document_service.process(content)

    document_repository = DocumentRepository()
    document_id = document_repository.save(file.filename)

    chunk_repository = ChunksRepository()
    chunk_repository.save_all(document_id, chunks_data)

    return {'id': document_id, 'file_name': file.filename}
