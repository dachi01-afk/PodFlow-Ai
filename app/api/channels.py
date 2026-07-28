from fastapi import APIRouter, HTTPException, Form
from datetime import datetime, timezone
import uuid

from app.core.supabase_client import get_supabase
from app.models.channel import ChannelResponse, ChannelList

router = APIRouter()


@router.get("/", response_model=ChannelList)
async def list_channels():
    supabase = get_supabase()
    result = supabase.table("channels").select("*").execute()

    channels = [ChannelResponse(**row) for row in result.data]

    return ChannelList(channels=channels, total=len(channels))


@router.post("/", response_model=ChannelResponse)
async def create_channel(
    name: str = Form(...),
    niche: str | None = Form(None),
    description: str | None = Form(None),
):
    supabase = get_supabase()

    now = datetime.now(timezone.utc).isoformat()

    data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "niche": niche,
        "description": description,
        "created_at": now,
    }

    result = supabase.table("channels").insert(data).execute()

    return ChannelResponse(**result.data[0])


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(channel_id: str):
    supabase = get_supabase()

    result = (
        supabase.table("channels")
        .select("*")
        .eq("id", channel_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Channel not found")

    return ChannelResponse(**result.data[0])