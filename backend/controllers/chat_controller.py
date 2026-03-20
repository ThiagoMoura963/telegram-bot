from fastapi import APIRouter
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.chat_service import ChatService
from backend.providers.gemini_provider import GeminiProvider

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

@router.post("")
def chat(request: ChatRequest) -> ChatResponse:
    provider = GeminiProvider()

    service = ChatService(provider)

    answer = service.get_answer(
        message=request.message,
        system_instruction=request.system_instruction
    )

    return ChatResponse(answer=answer)