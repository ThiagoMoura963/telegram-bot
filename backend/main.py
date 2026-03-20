from fastapi import FastAPI
from backend.controllers.chat_controller import router as chat_router
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World!"}

app.include_router(chat_router)
