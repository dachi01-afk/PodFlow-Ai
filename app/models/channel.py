from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChannelBase(BaseModel):
    name: str
    niche: Optional[str] = None
    description: Optional[str] = None


class ChannelCreate(ChannelBase):
    pass


class ChannelResponse(ChannelBase):
    id: str
    created_at: str


class ChannelList(BaseModel):
    channels: List[ChannelResponse]
    total: int
