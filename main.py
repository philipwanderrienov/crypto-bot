from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = Path(__file__).resolve().parent

for path in (str(BACKEND_ROOT), str(PROJECT_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from backend.api.models import HealthResponse
from backend.api.routes import router as api_router
from backend.config.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> dict[str, str]:
    return {"detail": "favicon not configured"}


@app.get("/", response_model=HealthResponse)
def root() -> dict[str, str]:
    return {"status": "ok"}