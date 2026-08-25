from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.health import router as health_router
from backend.api.v1.routes.url_scanner import router as url_scanner_router
from backend.api.v1.routes.scan_history import router as scan_history_router
from backend.api.v1.routes import auth

app = FastAPI(
    title="Sentinel AI",
    description="AI-Powered Digital Safety Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # Vite ka default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "🛡️ Sentinel AI is running!",
        "status": "success"
    }


app.include_router(health_router)

app.include_router(
    url_scanner_router,
    prefix="/api/v1"
)

app.include_router(
    scan_history_router,
    prefix="/api/v1"
)

app.include_router(auth.router)