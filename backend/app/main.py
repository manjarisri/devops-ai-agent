from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.incidents import router as incidents_router
from app.api.reviews import router as reviews_router


app = FastAPI(
    title="DevOps AI Assistant",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "application": "DevOps AI Assistant",
        "version": "1.0.0",
        "status": "running",
        "ai_provider": "local-demo",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(chat_router)
app.include_router(incidents_router)
app.include_router(reviews_router)