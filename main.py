from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from app.api import episodes, channels, pipeline

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "app", "audio_files")
RSS_DIR = os.path.join(os.path.dirname(__file__), "app", "rss_files")
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "app", "video_files")

app = FastAPI(title="PodFlow AI", version="1.0.0")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(episodes.router, prefix="/api/episodes", tags=["episodes"])
app.include_router(channels.router, prefix="/api/channels", tags=["channels"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["pipeline"])


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/episode/{episode_id}", response_class=HTMLResponse)
async def episode_page(request: Request, episode_id: str):
    return templates.TemplateResponse("episode.html", {"request": request, "episode_id": episode_id})


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}


@app.get("/rss/{channel_id}.xml")
async def serve_rss(channel_id: str):
    file_path = os.path.join(RSS_DIR, f"{channel_id}.xml")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/xml")
    return {"error": "RSS feed not found"}


@app.get("/video/{filename}")
async def serve_video(filename: str):
    file_path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4")
    return {"error": "File not found"}
