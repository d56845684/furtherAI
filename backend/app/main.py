from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import Base, engine
from . import models  # noqa: F401
from .routers import agent, conversations

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversations.router, prefix=settings.api_prefix)
app.include_router(agent.router, prefix=settings.api_prefix)


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}
