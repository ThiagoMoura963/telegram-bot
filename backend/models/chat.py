from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    system_instruction: str


class ChatResponse(BaseModel):
    answer: str
