from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router
from backend.config import settings


app = FastAPI(

    title="LegalEase API",

    version="1.0.0",

    description=(
        "AI-powered legal document "
        "generation and export API."
    )
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.get(
    "/",
    tags=["health"]
)
def root():

    return {
        "service": settings.app_name,
        "status": "running",
        "docs": "/docs"
    }


@app.get(
    "/health",
    tags=["health"]
)
def health():

    return {
        "status": "ok"
    }


app.include_router(router)