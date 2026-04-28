from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controllers.agent_controller import router as agent_router
from backend.controllers.agent_controller import router as bot_router
from backend.controllers.auth_controller import router as auth_router
from backend.controllers.document_controller import router as document_router
from backend.controllers.status_controller import router as status_router
from backend.controllers.telegram_controller import router as telegram_router

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

origins = [
    'https://telegram-bot-three-vert.vercel.app',
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'https://b27c-2804-14d-8e88-4ce0-ac7b-e59d-fef1-6cf8.ngrok-free.app',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5500'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
