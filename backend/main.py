from fastapi import FastAPI
from backend.controllers.telegram_controller import router as telegram_router
from backend.controllers.bot_controller import router as bot_router

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Hello World!'}

app.include_router(telegram_router)
app.include_router(bot_router)