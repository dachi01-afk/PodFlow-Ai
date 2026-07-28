# PodFlow AI - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build backend infrastructure for autonomous podcast production system with 4 AI agents.

**Architecture:** Python FastAPI backend deployed on Vercel, with Inngest for async agent orchestration, Supabase for database/storage, and CrewAI for agent management.

**Tech Stack:** Python 3.11+, FastAPI, CrewAI, Inngest, Supabase, FFmpeg, ElevenLabs API, Qwen API, Agnes AI API

## Global Constraints

- Python 3.11 or higher
- Virtual environment (venv) required
- All API keys stored in .env file (never committed)
- Deploy target: Vercel (serverless)
- Database: Supabase PostgreSQL
- Async processing: Inngest

---

## File Structure

```
podflow-ai/
├── main.py                 # FastAPI app entry point
├── config.py               # Pydantic settings management
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── vercel.json             # Vercel deployment config
├── runtime.txt             # Python version for Vercel
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── episodes.py     # Episode CRUD endpoints
│   │   ├── channels.py     # Channel CRUD endpoints
│   │   └── pipeline.py     # Pipeline trigger endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── inngest_client.py   # Inngest client setup
│   │   └── supabase_client.py  # Supabase client setup
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research.py     # Agent 1: Research Engine
│   │   ├── scriptwriter.py # Agent 2: Dialogue Scriptwriter
│   │   ├── audio.py        # Agent 3: Audio Engine
│   │   └── distribution.py # Agent 4: Distribution
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── pipeline.py     # Inngest pipeline functions
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── episode.py      # Episode Pydantic models
│   │   └── channel.py      # Channel Pydantic models
│   │
│   └── utils/
│       ├── __init__.py
│       ├── audio.py        # FFmpeg utilities
│       └── rss.py          # RSS feed generation
│
├── templates/
│   ├── base.html           # Base template
│   ├── dashboard.html      # Main dashboard
│   ├── episode.html        # Episode detail
│   └── create.html         # Create episode form
│
├── static/
│   └── css/
│       └── styles.css      # Custom styles
│
└── tests/
    ├── __init__.py
    ├── test_agents/
    │   ├── __init__.py
    │   ├── test_research.py
    │   ├── test_scriptwriter.py
    │   ├── test_audio.py
    │   └── test_distribution.py
    └── test_api/
        ├── __init__.py
        └── test_episodes.py
```

---

## Task 1: Project Setup & Configuration

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `config.py`
- Create: `vercel.json`
- Create: `runtime.txt`

**Interfaces:**
- Produces: `settings` object with all environment variables

---

- [ ] **Step 1: Create requirements.txt**

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
crewai==0.1.0
supabase==2.3.0
inngest==0.4.0
httpx==0.26.0
jinja2==3.1.3
python-multipart==0.0.6
```

---

- [ ] **Step 2: Create .env.example**

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# ElevenLabs
ELEVENLABS_API_KEY=your-api-key

# Qwen API
QWEN_API_KEY=your-api-key
QWEN_API_URL=https://api.qwen.com/v1

# Agnes AI
AGNES_API_KEY=your-api-key
AGNES_API_URL=https://api.agnes.ai/v1

# Inngest
INNGEST_EVENT_KEY=your-event-key
INNGEST_SIGNING_KEY=your-signing-key
```

---

- [ ] **Step 3: Create config.py**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # ElevenLabs
    elevenlabs_api_key: str
    
    # Qwen
    qwen_api_key: str
    qwen_api_url: str = "https://api.qwen.com/v1"
    
    # Agnes AI
    agnes_api_key: str
    agnes_api_url: str = "https://api.agnes.ai/v1"
    
    # Inngest
    inngest_event_key: str
    inngest_signing_key: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

- [ ] **Step 4: Create vercel.json**

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "main.py"
    },
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

---

- [ ] **Step 5: Create runtime.txt**

```
3.11
```

---

- [ ] **Step 6: Create virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example config.py vercel.json runtime.txt
git commit -m "feat: project setup with configuration"
```

---

## Task 2: Supabase Client Setup

**Files:**
- Create: `app/__init__.py`
- Create: `app/core/__init__.py`
- Create: `app/core/supabase_client.py`
- Create: `app/models/__init__.py`
- Create: `app/models/episode.py`
- Create: `app/models/channel.py`

**Interfaces:**
- Produces: `get_supabase()` function
- Produces: `Episode`, `Channel` Pydantic models

---

- [ ] **Step 1: Create app/__init__.py**

```python
```

---

- [ ] **Step 2: Create app/core/__init__.py**

```python
```

---

- [ ] **Step 3: Create app/core/supabase_client.py**

```python
from supabase import create_client, Client
from config import get_settings

_settings = get_settings()
_supabase_client: Client = None

def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(
            _settings.supabase_url,
            _settings.supabase_key
        )
    return _supabase_client
```

---

- [ ] **Step 4: Create app/models/__init__.py**

```python
```

---

- [ ] **Step 5: Create app/models/episode.py**

```python
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
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

class EpisodeList(BaseModel):
    episodes: List[EpisodeResponse]
    total: int
```

---

- [ ] **Step 6: Create app/models/channel.py**

```python
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
    created_at: datetime

class ChannelList(BaseModel):
    channels: List[ChannelResponse]
    total: int
```

---

- [ ] **Step 7: Commit**

```bash
git add app/ tests/
git commit -m "feat: supabase client and data models"
```

---

## Task 3: Inngest Client Setup

**Files:**
- Create: `app/core/inngest_client.py`
- Create: `app/tasks/__init__.py`
- Create: `app/tasks/pipeline.py`

**Interfaces:**
- Produces: `inngest_client` instance
- Produces: `pipeline` Inngest function

---

- [ ] **Step 1: Create app/core/inngest_client.py**

```python
import inngest
from config import get_settings

settings = get_settings()

inngest_client = inngest.Client(
    app_id="podflow-ai",
    event_key=settings.inngest_event_key,
    signing_key=settings.inngest_signing_key,
)
```

---

- [ ] **Step 2: Create app/tasks/__init__.py**

```python
```

---

- [ ] **Step 3: Create app/tasks/pipeline.py**

```python
import inngest
from app.core.inngest_client import inngest_client

@inngest_client.create_function(
    fn_id="podcast-pipeline",
    trigger=inngest.TriggerEvent(event="episode.created"),
)
async def podcast_pipeline(
    ctx: inngest.Context,
    step: inngest.Step,
) -> dict:
    episode_id = ctx.event.data.get("episode_id")
    
    # Step 1: Research
    research_result = await step.run(
        "research-agent",
        lambda: run_research_agent(episode_id),
    )
    
    # Step 2: Scriptwriting
    script_result = await step.run(
        "scriptwriter-agent",
        lambda: run_scriptwriter_agent(episode_id, research_result),
    )
    
    # Step 3: Audio Production
    audio_result = await step.run(
        "audio-agent",
        lambda: run_audio_agent(episode_id, script_result),
    )
    
    # Step 4: Distribution
    distribution_result = await step.run(
        "distribution-agent",
        lambda: run_distribution_agent(episode_id, audio_result),
    )
    
    return {"status": "completed", "episode_id": episode_id}

def run_research_agent(episode_id: str) -> dict:
    # Placeholder - will be implemented in Task 5
    return {"episode_id": episode_id, "status": "research_done"}

def run_scriptwriter_agent(episode_id: str, research: dict) -> dict:
    # Placeholder - will be implemented in Task 6
    return {"episode_id": episode_id, "status": "script_done"}

def run_audio_agent(episode_id: str, script: dict) -> dict:
    # Placeholder - will be implemented in Task 7
    return {"episode_id": episode_id, "status": "audio_done"}

def run_distribution_agent(episode_id: str, audio: dict) -> dict:
    # Placeholder - will be implemented in Task 8
    return {"episode_id": episode_id, "status": "distribution_done"}
```

---

- [ ] **Step 4: Commit**

```bash
git add app/core/inngest_client.py app/tasks/pipeline.py
git commit -m "feat: inngest client and pipeline function"
```

---

## Task 4: FastAPI Main App & API Endpoints

**Files:**
- Create: `main.py`
- Create: `app/api/__init__.py`
- Create: `app/api/episodes.py`
- Create: `app/api/channels.py`
- Create: `app/api/pipeline.py`

**Interfaces:**
- Consumes: `get_supabase()`, `EpisodeCreate`, `ChannelCreate`
- Produces: FastAPI app with all endpoints

---

- [ ] **Step 1: Create main.py**

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import inngest
import inngest.fastapi

from app.core.inngest_client import inngest_client
from app.tasks.pipeline import podcast_pipeline
from app.api import episodes, channels, pipeline

app = FastAPI(title="PodFlow AI", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(episodes.router, prefix="/api/episodes", tags=["episodes"])
app.include_router(channels.router, prefix="/api/channels", tags=["channels"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["pipeline"])

# Inngest
inngest_app = inngest.fastapi.create_fastapi_endpoint(
    app=app,
    client=inngest_client,
    functions=[podcast_pipeline],
)

@app.get("/")
async def dashboard():
    return templates.TemplateResponse("dashboard.html", {"request": {}})

@app.get("/episode/{episode_id}")
async def episode_detail(episode_id: str):
    return templates.TemplateResponse("episode.html", {"request": {}, "episode_id": episode_id})

@app.get("/create")
async def create_episode():
    return templates.TemplateResponse("create.html", {"request": {}})
```

---

- [ ] **Step 2: Create app/api/__init__.py**

```python
```

---

- [ ] **Step 3: Create app/api/episodes.py**

```python
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import uuid

from app.core.supabase_client import get_supabase
from app.models.episode import EpisodeCreate, EpisodeResponse, EpisodeList

router = APIRouter()

@router.get("/", response_model=EpisodeList)
async def list_episodes():
    supabase = get_supabase()
    result = supabase.table("episodes").select("*").order("created_at", desc=True).execute()
    return EpisodeList(episodes=result.data, total=len(result.data))

@router.post("/", response_model=EpisodeResponse)
async def create_episode(episode: EpisodeCreate):
    supabase = get_supabase()
    now = datetime.utcnow().isoformat()
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
    result = supabase.table("episodes").select("*").eq("id", episode_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Episode not found")
    return EpisodeResponse(**result.data[0])

@router.delete("/{episode_id}")
async def delete_episode(episode_id: str):
    supabase = get_supabase()
    supabase.table("episodes").delete().eq("id", episode_id).execute()
    return {"status": "deleted"}
```

---

- [ ] **Step 4: Create app/api/channels.py**

```python
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import uuid

from app.core.supabase_client import get_supabase
from app.models.channel import ChannelCreate, ChannelResponse, ChannelList

router = APIRouter()

@router.get("/", response_model=ChannelList)
async def list_channels():
    supabase = get_supabase()
    result = supabase.table("channels").select("*").execute()
    return ChannelList(channels=result.data, total=len(result.data))

@router.post("/", response_model=ChannelResponse)
async def create_channel(channel: ChannelCreate):
    supabase = get_supabase()
    now = datetime.utcnow().isoformat()
    data = {
        "id": str(uuid.uuid4()),
        "name": channel.name,
        "niche": channel.niche,
        "description": channel.description,
        "created_at": now,
    }
    result = supabase.table("channels").insert(data).execute()
    return ChannelResponse(**result.data[0])

@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(channel_id: str):
    supabase = get_supabase()
    result = supabase.table("channels").select("*").eq("id", channel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelResponse(**result.data[0])
```

---

- [ ] **Step 5: Create app/api/pipeline.py**

```python
from fastapi import APIRouter, HTTPException
from app.core.supabase_client import get_supabase
from app.core.inngest_client import inngest_client

router = APIRouter()

@router.post("/start/{episode_id}")
async def start_pipeline(episode_id: str):
    supabase = get_supabase()
    
    # Check episode exists
    result = supabase.table("episodes").select("*").eq("id", episode_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    episode = result.data[0]
    if episode["status"] != "pending":
        raise HTTPException(status_code=400, detail="Episode already processing")
    
    # Update status to researching
    supabase.table("episodes").update({"status": "researching"}).eq("id", episode_id).execute()
    
    # Send event to Inngest
    await inngest_client.send({
        "name": "episode.created",
        "data": {"episode_id": episode_id},
    })
    
    return {"status": "started", "episode_id": episode_id}

@router.get("/status/{episode_id}")
async def get_status(episode_id: str):
    supabase = get_supabase()
    result = supabase.table("episodes").select("id, status, error").eq("id", episode_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Episode not found")
    return result.data[0]
```

---

- [ ] **Step 6: Commit**

```bash
git add main.py app/api/
git commit -m "feat: fastapi app with episode, channel, and pipeline endpoints"
```

---

## Task 5: Agent 1 - Research Engine (Qwen)

**Files:**
- Create: `app/agents/__init__.py`
- Create: `app/agents/research.py`
- Modify: `app/tasks/pipeline.py` (implement run_research_agent)

**Interfaces:**
- Consumes: `episode_id`, Qwen API
- Produces: `research_output` dict with facts and trends

---

- [ ] **Step 1: Create app/agents/__init__.py**

```python
```

---

- [ ] **Step 2: Create app/agents/research.py**

```python
import httpx
from typing import List, Dict
from config import get_settings

settings = get_settings()

async def research_topic(topic: str) -> Dict:
    """Research a topic using Qwen API"""
    
    prompt = f"""
    Anda adalah peneliti ahli. Teliti topik berikut dan berikan hasilnya dalam format JSON:
    
    Topik: {topic}
    
    Struktur output:
    {{
        "topic": "{topic}",
        "summary": "Ringkasan topik dalam 2-3 kalimat",
        "key_facts": ["fakta 1", "fakta 2", "fakta 3"],
        "trends": ["tren 1", "tren 2"],
        "sentiment": "positif/negatif/netral",
        "sources": ["sumber 1", "sumber 2"]
    }}
    
    Berikan minimal 5 fakta kunci dan 3 tren.
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.qwen_api_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.qwen_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "qwen-2.5-72b-instruct",
                "messages": [
                    {"role": "system", "content": "Anda adalah peneliti ahli yang menghasilkan riset berkualitas tinggi."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
            },
            timeout=120.0,
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Parse the content from Qwen response
        content = data["choices"][0]["message"]["content"]
        
        # Extract JSON from content
        import json
        import re
        
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            return json.loads(json_match.group())
        
        return {
            "topic": topic,
            "summary": content[:500],
            "key_facts": [],
            "trends": [],
            "sentiment": "netral",
            "sources": [],
        }
```

---

- [ ] **Step 3: Update app/tasks/pipeline.py**

```python
import inngest
from app.core.inngest_client import inngest_client
from app.core.supabase_client import get_supabase
from app.agents.research import research_topic

# ... existing code ...

def run_research_agent(episode_id: str) -> dict:
    """Run research agent for the given episode"""
    supabase = get_supabase()
    
    # Get episode topic
    result = supabase.table("episodes").select("topic").eq("id", episode_id).execute()
    if not result.data:
        raise Exception(f"Episode {episode_id} not found")
    
    topic = result.data[0]["topic"]
    
    # Update status
    supabase.table("episodes").update({"status": "researching"}).eq("id", episode_id).execute()
    
    # Run research (synchronous wrapper for Inngest)
    import asyncio
    research_result = asyncio.run(research_topic(topic))
    
    # Store result
    supabase.table("episodes").update({
        "metadata": {"research": research_result},
        "status": "writing",
    }).eq("id", episode_id).execute()
    
    return research_result
```

---

- [ ] **Step 4: Commit**

```bash
git add app/agents/research.py app/tasks/pipeline.py
git commit -m "feat: agent 1 research engine with qwen api"
```

---

## Task 6: Agent 2 - Dialogue Scriptwriter (Agnes AI)

**Files:**
- Create: `app/agents/scriptwriter.py`
- Modify: `app/tasks/pipeline.py` (implement run_scriptwriter_agent)

**Interfaces:**
- Consumes: `episode_id`, `research_output`
- Produces: `script_output` JSON with dialogue and emotions

---

- [ ] **Step 1: Create app/agents/scriptwriter.py**

```python
import httpx
from typing import Dict, List
import json
import re
from config import get_settings

settings = get_settings()

async def generate_script(topic: str, research: Dict) -> List[Dict]:
    """Generate dialogue script using Agnes AI"""
    
    prompt = f"""
    Anda adalah penulis dialog podcast ahli. Buatlah dialog podcast interaktif berdasarkan riset berikut:
    
    Topik: {topic}
    Riset: {json.dumps(research, ensure_ascii=False)}
    
    Buatlah dialog antara 2 host:
    - Host A: Pakar formal, memberikan penjelasan
    - Host B: Pemula kritis, bertanya dan memberikan sudut pandang berbeda
    
    Format output harus berupa JSON array dengan struktur:
    [
        {{
            "speaker": "Host_A atau Host_B",
            "emotion": "enthusiastic/confused/neutral/thinking/excited",
            "pause_duration": 0.5-2.0,
            "text": "Teks dialog"
        }}
    ]
    
    Buat minimal 10 dialog dengan variasi emosi yang natural.
    Gunakan bahasa Indonesia sehari-hari dengan sedikit humor.
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.agnes_api_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.agnes_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "agnes-2.0-flash",
                "messages": [
                    {"role": "system", "content": "Anda adalah penulis dialog podcast profesional dengan gaya bahasa Indonesia yang natural dan humoris."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 3000,
            },
            timeout=120.0,
        )
        
        response.raise_for_status()
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        
        # Parse JSON from content
        json_match = re.search(r'\[[\s\S]*\]', content)
        if json_match:
            return json.loads(json_match.group())
        
        # Fallback: return basic script
        return [
            {"speaker": "Host_A", "emotion": "neutral", "pause_duration": 1.0, "text": f"Selamat datang di podcast kita hari ini tentang {topic}."},
            {"speaker": "Host_B", "emotion": "curious", "pause_duration": 0.5, "text": "Wah, menarik sekali! Bisa ceritakan lebih lanjut?"},
        ]
```

---

- [ ] **Step 2: Update app/tasks/pipeline.py**

```python
from app.agents.scriptwriter import generate_script

# ... existing code ...

def run_scriptwriter_agent(episode_id: str, research: dict) -> dict:
    """Run scriptwriter agent for the given episode"""
    supabase = get_supabase()
    
    # Get episode topic
    result = supabase.table("episodes").select("topic").eq("id", episode_id).execute()
    if not result.data:
        raise Exception(f"Episode {episode_id} not found")
    
    topic = result.data[0]["topic"]
    
    # Update status
    supabase.table("episodes").update({"status": "writing"}).eq("id", episode_id).execute()
    
    # Generate script
    import asyncio
    script_result = asyncio.run(generate_script(topic, research))
    
    # Store result
    supabase.table("episodes").update({
        "script": {"dialogues": script_result},
        "status": "producing",
    }).eq("id", episode_id).execute()
    
    return {"dialogues": script_result}
```

---

- [ ] **Step 3: Commit**

```bash
git add app/agents/scriptwriter.py app/tasks/pipeline.py
git commit -m "feat: agent 2 scriptwriter with agnes ai"
```

---

## Task 7: Agent 3 - Audio Engine (ElevenLabs + FFmpeg)

**Files:**
- Create: `app/agents/audio.py`
- Create: `app/utils/audio.py`
- Modify: `app/tasks/pipeline.py` (implement run_audio_agent)

**Interfaces:**
- Consumes: `episode_id`, `script_output`
- Produces: `audio_url` pointing to Supabase Storage

---

- [ ] **Step 1: Create app/utils/audio.py**

```python
import subprocess
import tempfile
import os
from typing import List

def concatenate_audio_files(audio_files: List[str], output_path: str) -> str:
    """Concatenate multiple audio files using FFmpeg"""
    
    # Create file list for FFmpeg
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")
        file_list = f.name
    
    try:
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", file_list,
            "-c", "copy",
            output_path,
            "-y"
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    finally:
        os.unlink(file_list)

def apply_audio_ducking(vocal_path: str, bgm_path: str, output_path: str) -> str:
    """Apply audio ducking - lower BGM volume when vocal is active"""
    
    cmd = [
        "ffmpeg",
        "-i", vocal_path,
        "-i", bgm_path,
        "-filter_complex",
        "[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2:duration=first",
        output_path,
        "-y"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

def generate_silence(duration: float, output_path: str) -> str:
    """Generate silence audio file"""
    
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=mono",
        "-t", str(duration),
        output_path,
        "-y"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
```

---

- [ ] **Step 2: Create app/agents/audio.py**

```python
import httpx
import tempfile
import os
from typing import List, Dict
from config import get_settings
from app.utils.audio import concatenate_audio_files, generate_silence

settings = get_settings()

# Voice IDs for different hosts
VOICE_IDS = {
    "Host_A": "21m00Tcm4TlvDq8ikWAM",  # Rachel - professional female
    "Host_B": "ErXwobaYiN019PkySvjV",  # Antoni - friendly male
}

async def text_to_speech(text: str, voice_id: str) -> bytes:
    """Convert text to speech using ElevenLabs API"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": settings.elevenlabs_api_key,
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            },
            timeout=60.0,
        )
        
        response.raise_for_status()
        return response.content

async def generate_episode_audio(dialogues: List[Dict]) -> str:
    """Generate audio for entire episode from dialogues"""
    
    audio_files = []
    
    for dialogue in dialogues:
        speaker = dialogue.get("speaker", "Host_A")
        text = dialogue.get("text", "")
        pause_duration = dialogue.get("pause_duration", 0.5)
        
        # Get voice ID
        voice_id = VOICE_IDS.get(speaker, VOICE_IDS["Host_A"])
        
        # Generate speech
        audio_data = await text_to_speech(text, voice_id)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(audio_data)
            audio_files.append(f.name)
        
        # Add pause if needed
        if pause_duration > 0:
            pause_file = tempfile.mktemp(suffix='.mp3')
            generate_silence(pause_duration, pause_file)
            audio_files.append(pause_file)
    
    # Concatenate all audio files
    output_path = tempfile.mktemp(suffix='.mp3')
    concatenate_audio_files(audio_files, output_path)
    
    # Cleanup temp files
    for f in audio_files:
        if os.path.exists(f):
            os.unlink(f)
    
    return output_path
```

---

- [ ] **Step 3: Update app/tasks/pipeline.py**

```python
from app.agents.audio import generate_episode_audio
from app.core.supabase_client import get_supabase

# ... existing code ...

def run_audio_agent(episode_id: str, script: dict) -> dict:
    """Run audio agent for the given episode"""
    supabase = get_supabase()
    
    # Update status
    supabase.table("episodes").update({"status": "producing"}).eq("id", episode_id).execute()
    
    # Generate audio
    dialogues = script.get("dialogues", [])
    import asyncio
    audio_path = asyncio.run(generate_episode_audio(dialogues))
    
    # Upload to Supabase Storage
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    
    storage_path = f"episodes/{episode_id}/audio.mp3"
    supabase.storage.from_("audio").upload(storage_path, audio_data)
    
    # Get public URL
    audio_url = supabase.storage.from_("audio").get_public_url(storage_path)
    
    # Update episode
    supabase.table("episodes").update({
        "audio_url": audio_url,
        "status": "publishing",
    }).eq("id", episode_id).execute()
    
    # Cleanup
    os.unlink(audio_path)
    
    return {"audio_url": audio_url}
```

---

- [ ] **Step 4: Commit**

```bash
git add app/agents/audio.py app/utils/audio.py app/tasks/pipeline.py
git commit -m "feat: agent 3 audio engine with elevenlabs and ffmpeg"
```

---

## Task 8: Agent 4 - Distribution (SEO + RSS)

**Files:**
- Create: `app/agents/distribution.py`
- Create: `app/utils/rss.py`
- Modify: `app/tasks/pipeline.py` (implement run_distribution_agent)

**Interfaces:**
- Consumes: `episode_id`, `audio_url`
- Produces: Updated episode with metadata and RSS feed

---

- [ ] **Step 1: Create app/utils/rss.py**

```python
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from typing import List, Dict

def generate_rss_feed(channel_name: str, episodes: List[Dict]) -> str:
    """Generate RSS feed XML for podcast"""
    
    rss = Element("rss", version="2.0")
    rss.set("xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = channel_name
    SubElement(channel, "description").text = f"Podcast by {channel_name}"
    SubElement(channel, "language").text = "id"
    SubElement(channel, "itunes:author").text = channel_name
    
    for episode in episodes:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = episode.get("title", "Untitled")
        SubElement(item, "description").text = episode.get("description", "")
        SubElement(item, "enclosure", {
            "url": episode.get("audio_url", ""),
            "type": "audio/mpeg",
            "length": str(episode.get("audio_length", 0)),
        })
        SubElement(item, "pubDate").text = episode.get("published_at", "")
        SubElement(item, "itunes:duration").text = episode.get("duration", "00:00")
    
    xml_string = tostring(rss, encoding="unicode", method="xml")
    return parseString(xml_string).toprettyxml(indent="  ")
```

---

- [ ] **Step 2: Create app/agents/distribution.py**

```python
from typing import Dict
from app.core.supabase_client import get_supabase
from app.utils.rss import generate_rss_feed

async def generate_metadata(topic: str, script: Dict) -> Dict:
    """Generate SEO metadata for the episode"""
    
    # Generate title
    title = f"PodFlow: {topic}"
    
    # Generate description from script
    dialogues = script.get("dialogues", [])
    description_parts = [d.get("text", "")[:100] for d in dialogues[:3]]
    description = " ".join(description_parts) + "..."
    
    # Generate show notes
    show_notes = f"""
## Episode: {topic}

### Highlights
{chr(10).join(['- ' + d.get('text', '')[:80] for d in dialogues[:5]])}

### Timestamps
- 00:00 - Introduction
- 02:00 - Main Discussion
- 08:00 - Key Insights
- 10:00 - Conclusion
    """
    
    return {
        "title": title,
        "description": description,
        "show_notes": show_notes,
        "tags": [topic.lower().split()[:5]],
    }

async def publish_episode(episode_id: str, audio_url: str, metadata: Dict) -> str:
    """Publish episode and update RSS feed"""
    
    supabase = get_supabase()
    
    # Get channel info
    result = supabase.table("episodes").select("channel_id").eq("id", episode_id).execute()
    if result.data:
        channel_id = result.data[0]["channel_id"]
        channel_result = supabase.table("channels").select("name").eq("id", channel_id).execute()
        channel_name = channel_result.data[0]["name"] if channel_result.data else "PodFlow"
    else:
        channel_name = "PodFlow"
    
    # Get all episodes for RSS
    episodes_result = supabase.table("episodes").select("*").eq("channel_id", channel_id).order("created_at", desc=True).execute()
    
    episodes_for_rss = []
    for ep in episodes_result.data:
        episodes_for_rss.append({
            "title": ep.get("metadata", {}).get("title", "Untitled"),
            "description": ep.get("metadata", {}).get("description", ""),
            "audio_url": ep.get("audio_url", ""),
            "audio_length": 0,
            "published_at": ep.get("created_at", ""),
            "duration": "00:00",
        })
    
    # Generate RSS
    rss_feed = generate_rss_feed(channel_name, episodes_for_rss)
    
    # Store RSS in Supabase
    rss_path = f"channels/{channel_id}/feed.xml"
    supabase.storage.from_("rss").upload(rss_path, rss_feed.encode())
    
    return supabase.storage.from_("rss").get_public_url(rss_path)
```

---

- [ ] **Step 3: Update app/tasks/pipeline.py**

```python
from app.agents.distribution import generate_metadata, publish_episode

# ... existing code ...

def run_distribution_agent(episode_id: str, audio: dict) -> dict:
    """Run distribution agent for the given episode"""
    supabase = get_supabase()
    
    # Update status
    supabase.table("episodes").update({"status": "publishing"}).eq("id", episode_id).execute()
    
    # Get episode data
    result = supabase.table("episodes").select("topic, script").eq("id", episode_id).execute()
    if not result.data:
        raise Exception(f"Episode {episode_id} not found")
    
    episode = result.data[0]
    topic = episode["topic"]
    script = episode.get("script", {})
    
    # Generate metadata
    import asyncio
    metadata = asyncio.run(generate_metadata(topic, script))
    
    # Publish and generate RSS
    audio_url = audio.get("audio_url", "")
    rss_url = asyncio.run(publish_episode(episode_id, audio_url, metadata))
    
    # Update episode as completed
    from datetime import datetime
    supabase.table("episodes").update({
        "metadata": metadata,
        "status": "completed",
        "completed_at": datetime.utcnow().isoformat(),
    }).eq("id", episode_id).execute()
    
    return {"metadata": metadata, "rss_url": rss_url}
```

---

- [ ] **Step 4: Commit**

```bash
git add app/agents/distribution.py app/utils/rss.py app/tasks/pipeline.py
git commit -m "feat: agent 4 distribution with seo and rss feed"
```

---

## Task 9: Frontend Dashboard (Jinja2 + HTMX + Tailwind)

**Files:**
- Create: `templates/base.html`
- Create: `templates/dashboard.html`
- Create: `templates/episode.html`
- Create: `templates/create.html`
- Create: `static/css/styles.css`

**Interfaces:**
- Consumes: API endpoints
- Produces: HTML dashboard UI

---

- [ ] **Step 1: Create templates/base.html**

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PodFlow AI - {% block title %}Dashboard{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <nav class="bg-gray-800 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-purple-400">🎙️ PodFlow AI</a>
            <div class="space-x-4">
                <a href="/" class="hover:text-purple-400">Dashboard</a>
                <a href="/create" class="bg-purple-600 px-4 py-2 rounded hover:bg-purple-700">+ New Episode</a>
            </div>
        </div>
    </nav>
    
    <main class="container mx-auto p-6">
        {% block content %}{% endblock %}
    </main>
    
    <script>
        // Auto-refresh dashboard
        document.addEventListener('DOMContentLoaded', function() {
            setInterval(function() {
                htmx.trigger('#episodes-list', 'refresh');
            }, 5000);
        });
    </script>
</body>
</html>
```

---

- [ ] **Step 2: Create templates/dashboard.html**

```html
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="mb-6">
    <h1 class="text-3xl font-bold mb-2">Podcast Dashboard</h1>
    <p class="text-gray-400">Kelola episode podcast Anda secara otonom</p>
</div>

<!-- Stats -->
<div class="grid grid-cols-4 gap-4 mb-6">
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-purple-400">--</div>
        <div class="text-gray-400">Total Episodes</div>
    </div>
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-green-400">--</div>
        <div class="text-gray-400">Completed</div>
    </div>
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-yellow-400">--</div>
        <div class="text-gray-400">Processing</div>
    </div>
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-red-400">--</div>
        <div class="text-gray-400">Failed</div>
    </div>
</div>

<!-- Episodes List -->
<div id="episodes-list" 
     hx-get="/api/episodes" 
     hx-trigger="refresh from:body" 
     hx-swap="innerHTML"
     class="bg-gray-800 rounded-lg p-4">
    <div class="text-center text-gray-400 py-8">Loading episodes...</div>
</div>

{% endblock %}
```

---

- [ ] **Step 3: Create templates/episode.html**

```html
{% extends "base.html" %}

{% block title %}Episode Detail{% endblock %}

{% block content %}
<div id="episode-detail" 
     hx-get="/api/episodes/{{ episode_id }}" 
     hx-trigger="load, every 5s" 
     hx-swap="innerHTML">
    <div class="text-center text-gray-400 py-8">Loading episode...</div>
</div>
{% endblock %}
```

---

- [ ] **Step 4: Create templates/create.html**

```html
{% extends "base.html" %}

{% block title %}Create Episode{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Create New Episode</h1>
    
    <form hx-post="/api/episodes" 
          hx-swap="none"
          hx-on::after-request="if(event.detail.successful) window.location='/'"
          class="bg-gray-800 p-6 rounded-lg space-y-4">
        
        <div>
            <label class="block text-gray-400 mb-2">Channel</label>
            <select name="channel_id" required
                    class="w-full bg-gray-700 rounded px-4 py-2 focus:ring-2 focus:ring-purple-500">
                <option value="">Select Channel</option>
            </select>
        </div>
        
        <div>
            <label class="block text-gray-400 mb-2">Topic</label>
            <input type="text" name="topic" required
                   placeholder="Contoh: Strategi Keuangan Mikro untuk Usaha Kecil"
                   class="w-full bg-gray-700 rounded px-4 py-2 focus:ring-2 focus:ring-purple-500">
        </div>
        
        <button type="submit" 
                class="w-full bg-purple-600 hover:bg-purple-700 py-3 rounded font-bold">
            🚀 Create & Start Production
        </button>
    </form>
</div>
{% endblock %}
```

---

- [ ] **Step 5: Create static/css/styles.css**

```css
/* Custom styles for PodFlow AI */

/* Progress bar animation */
.progress-bar {
    transition: width 0.5s ease-in-out;
}

/* Status badges */
.status-pending { @apply bg-gray-500; }
.status-researching { @apply bg-blue-500; }
.status-writing { @apply bg-yellow-500; }
.status-producing { @apply bg-orange-500; }
.status-publishing { @apply bg-purple-500; }
.status-completed { @apply bg-green-500; }
.status-failed { @apply bg-red-500; }

/* Pulse animation for processing */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.animate-pulse {
    animation: pulse 2s infinite;
}
```

---

- [ ] **Step 6: Commit**

```bash
git add templates/ static/
git commit -m "feat: frontend dashboard with jinja2, htmx, and tailwind"
```

---

## Task 10: Database Setup Script

**Files:**
- Create: `scripts/setup_database.py`

**Interfaces:**
- Produces: Supabase tables and storage buckets

---

- [ ] **Step 1: Create scripts/setup_database.py**

```python
"""Setup Supabase database tables and storage buckets"""
from app.core.supabase_client import get_supabase

def setup_database():
    supabase = get_supabase()
    
    # Note: Supabase free tier doesn't support programmatic table creation via client
    # You need to create tables manually in Supabase dashboard or use SQL editor
    
    print("📋 Please run the following SQL in Supabase SQL Editor:")
    print("-" * 60)
    print("""
-- Channels table
CREATE TABLE channels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  niche TEXT,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Episodes table
CREATE TABLE episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  channel_id UUID REFERENCES channels(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'researching', 'writing', 'producing', 'publishing', 'completed', 'failed')),
  topic TEXT NOT NULL,
  script JSONB,
  audio_url TEXT,
  metadata JSONB,
  error TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- Enable Row Level Security
ALTER TABLE channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE episodes ENABLE ROW LEVEL SECURITY;

-- Allow all operations (for demo)
CREATE POLICY "Allow all" ON channels FOR ALL USING (true);
CREATE POLICY "Allow all" ON episodes FOR ALL USING (true);
    """)
    print("-" * 60)
    print("\n📁 Create storage buckets in Supabase Dashboard:")
    print("   - audio (for episode audio files)")
    print("   - rss (for RSS feed files)")

if __name__ == "__main__":
    setup_database()
```

---

- [ ] **Step 2: Commit**

```bash
git add scripts/
git commit -m "feat: database setup script"
```

---

## Task 11: Final Testing & Deployment

**Files:**
- Modify: `requirements.txt` (add any missing dependencies)
- Create: `README.md`

**Interfaces:**
- Produces: Working deployment on Vercel

---

- [ ] **Step 1: Test locally**

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
uvicorn main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/api/episodes
curl http://localhost:8000/api/channels
```

---

- [ ] **Step 2: Deploy to Vercel**

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

---

- [ ] **Step 3: Create README.md**

```markdown
# PodFlow AI

The Autonomous Podcast Network - Sistem AI otonom untuk produksi podcast end-to-end.

## Fitur

- 🎙️ 4 AI Agents (Research, Scriptwriter, Audio, Distribution)
- 🔄 Parallel processing dengan Inngest
- 📊 Real-time dashboard
- 🎨 Audio generation dengan ElevenLabs + FFmpeg
- 📝 Auto-generated SEO metadata & RSS feed

## Tech Stack

- Backend: Python FastAPI
- Agents: CrewAI
- Async: Inngest
- Database: Supabase
- Deployment: Vercel

## Setup

```bash
# Clone
git clone <repo-url>
cd podflow-ai

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup env
cp .env.example .env
# Edit .env with your API keys

# Run locally
uvicorn main:app --reload
```

## API Keys

Dapatkan API keys dari:
- Supabase: https://supabase.com
- ElevenLabs: https://elevenlabs.io
- Qwen: https://qwen.ai
- Agnes AI: https://agnes.ai
- Inngest: https://inngest.com

## License

MIT
```

---

- [ ] **Step 4: Final commit**

```bash
git add README.md
git commit -m "docs: add readme and finalize deployment"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Project Setup | requirements.txt, .env.example, config.py, vercel.json, runtime.txt |
| 2 | Supabase Client | supabase_client.py, episode.py, channel.py |
| 3 | Inngest Client | inngest_client.py, pipeline.py |
| 4 | FastAPI Endpoints | main.py, episodes.py, channels.py, pipeline.py |
| 5 | Agent 1: Research | research.py |
| 6 | Agent 2: Scriptwriter | scriptwriter.py |
| 7 | Agent 3: Audio | audio.py, utils/audio.py |
| 8 | Agent 4: Distribution | distribution.py, utils/rss.py |
| 9 | Frontend Dashboard | templates/, static/ |
| 10 | Database Setup | scripts/setup_database.py |
| 11 | Final Testing | README.md |

**Total: 11 Tasks, ~50 Files**
