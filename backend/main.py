from fastapi import FastAPI

from backend.controllers.auth_controller import router as auth_router
from backend.controllers.agent_controller import router as bot_router
from backend.controllers.document_controller import router as document_router
from backend.controllers.status_controller import router as status_router
from backend.controllers.telegram_controller import router as telegram_router
from backend.controllers.agent_controller import router as agent_router

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Hello World'}

app.include_router(telegram_router)
app.include_router(bot_router)
app.include_router(status_router)
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(agent_router)