from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EpisodeStatus(str, Enum):
    PENDING = "pending"
    RESEARCHING = "researching"
    WRITING = "writing"
    PRODUCING = "producing"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"


class EpisodeBase(BaseModel):
    channel_id: str
    topic: str


class EpisodeCreate(EpisodeBase):
    pass


class EpisodeResponse(EpisodeBase):
    id: str
    status: EpisodeStatus
    script: Optional[dict] = None
    audio_url: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None


class EpisodeList(BaseModel):
    episodes: List[EpisodeResponse]
    total: int
