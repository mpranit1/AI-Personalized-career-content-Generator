import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import config
from backend.api.routes import router as api_router

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title=config.app_name,
    version=config.version,
    description="AI-Based Personalized Career Content Generator: Produces tailored summaries, skill gap reports, learning roadmaps, and interview prep with cross-format consistency verification.",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix=config.api_prefix)

# Serve Frontend static assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", response_class=FileResponse)
    async def serve_index():
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": f"{config.app_name} API is running. UI index not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=config.host, port=config.port, reload=config.debug)
