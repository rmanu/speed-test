import os
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_PATH = Path(__file__).parent.parent / "frontend" / "index.html"
CHUNK_SIZE = 64 * 1024  # 64 KB chunks

# --- API routes (mounted at both "" and "/api/speedtest") ---

router = APIRouter()


@router.get("/ping")
async def ping():
    return JSONResponse({"pong": True})


@router.get("/download")
async def download(size: int = 10):
    size = max(1, min(size, 100))
    total_bytes = size * 1024 * 1024

    def generate():
        remaining = total_bytes
        chunk = os.urandom(CHUNK_SIZE)
        while remaining > 0:
            send = min(CHUNK_SIZE, remaining)
            yield chunk[:send]
            remaining -= send

    return StreamingResponse(
        generate(),
        media_type="application/octet-stream",
        headers={
            "Content-Length": str(total_bytes),
            "Cache-Control": "no-store",
        },
    )


@router.post("/upload")
async def upload(request: Request):
    body = await request.body()
    return JSONResponse({"received": len(body)})


# Mount the same router at both prefixes
app.include_router(router)                        # /ping, /download, /upload
app.include_router(router, prefix="/api/speedtest")  # /api/speedtest/ping, …


@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_PATH)
