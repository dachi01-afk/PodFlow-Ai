import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

from celery_app import celery_app
from app.core.supabase_client import get_supabase

router = APIRouter()


@router.post("/start/{episode_id}")
async def start_pipeline(episode_id: str):
    supabase = get_supabase()

    result = (
        supabase.table("episodes")
        .select("*")
        .eq("id", episode_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Episode not found")

    episode = result.data[0]

    if episode["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="Episode already processing"
        )

    supabase.table("episodes").update(
        {"status": "researching"}
    ).eq(
        "id",
        episode_id
    ).execute()

    celery_app.send_task(
        "app.tasks.pipeline.run_research_agent",
        args=[episode_id],
    )

    return {
        "status": "started",
        "episode_id": episode_id,
    }


@router.get("/status/{episode_id}")
async def get_status(episode_id: str):
    supabase = get_supabase()

    result = (
        supabase.table("episodes")
        .select("id, status, error")
        .eq("id", episode_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Episode not found"
        )

    return result.data[0]


@router.post("/upload/{episode_id}")
async def upload_tiktok(episode_id: str):
    supabase = get_supabase()

    result = (
        supabase.table("episodes")
        .select("*")
        .eq("id", episode_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Episode not found"
        )

    episode = result.data[0]

    metadata = episode.get("metadata") or {}

    video_url = metadata.get("video_url")

    if not video_url:
        raise HTTPException(
            status_code=400,
            detail="Episode has no video"
        )

    filename = Path(video_url).name
    video_path = Path("app/video_files") / filename

    if not video_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Video not found: {video_path}"
        )

    caption = (
        episode.get("script", {}).get("tiktok_caption")
        or "🎙️ Generated with PodFlow AI"
    )

    try:
        subprocess.Popen(
            [
                sys.executable,
                "scripts/tiktok_uploader.py",
                str(video_path),
                caption,
            ],
            cwd=Path.cwd(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return {
        "status": "started",
        "message": "TikTok upload launched!"
    }