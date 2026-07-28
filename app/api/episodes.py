from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid

from app.core.supabase_client import get_supabase
from app.models.episode import EpisodeCreate, EpisodeResponse, EpisodeList

router = APIRouter()


@router.get("/", response_model=EpisodeList)
async def list_episodes():
    supabase = get_supabase()
    result = (
        supabase.table("episodes")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    episodes = []
    for row in result.data:
        episodes.append(EpisodeResponse(**row))
    return EpisodeList(episodes=episodes, total=len(episodes))


@router.post("/", response_model=EpisodeResponse)
async def create_episode(episode: EpisodeCreate):
    supabase = get_supabase()
    now = datetime.now(timezone.utc).isoformat()
    data = {
        "id": str(uuid.uuid4()),
        "channel_id": episode.channel_id,
        "topic": episode.topic,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }
    result = supabase.table("episodes").insert(data).execute()
    return EpisodeResponse(**result.data[0])


@router.get("/{episode_id}", response_model=EpisodeResponse)
async def get_episode(episode_id: str):
    supabase = get_supabase()
    result = (
        supabase.table("episodes")
        .select("*")
        .eq("id", episode_id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Episode not found")
    return EpisodeResponse(**result.data[0])


@router.delete("/{episode_id}")
async def delete_episode(episode_id: str):
    supabase = get_supabase()
    supabase.table("episodes").delete().eq("id", episode_id).execute()
    return {"status": "deleted"}
