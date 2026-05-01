# type: ignore

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile

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
async def upload_document(
    files: Annotated[list[UploadFile], File()],
    agent_id: Annotated[str, Form()],
    user_id: Annotated[str, Depends(get_current_user_id)],
):
    uploaded_documents = []

    document_repository = DocumentRepository()
    chunk_repository = ChunksRepository()

    for file in files:
        content = await file.read()

        document_processor = get_document_processor(file.content_type)

        document_service = DocumentService(document_processor)

        chunks_data = document_service.process(content)

        document_id = document_repository.save(file.filename)

        chunk_repository.save_all(document_id=document_id, chunks_data=chunks_data, user_id=user_id, agent_id=agent_id)

        uploaded_documents.append({'id': str(document_id), 'file_name': file.filename})

    return {'documents': uploaded_documents}


@router.delete('/{agent_id}/{document_id}')
async def delete_document(agent_id: str, document_id: str, user_id: Annotated[str, Depends(get_current_user_id)]):

    document_repository = DocumentRepository()
    document_repository.delete(document_id, agent_id)

    return {'message': 'Document deleted successfully.'}
