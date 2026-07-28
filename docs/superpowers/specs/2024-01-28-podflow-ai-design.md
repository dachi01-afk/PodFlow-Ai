# PodFlow AI - Design Document

## Overview

PodFlow AI adalah sistem AI otonom untuk produksi podcast end-to-end dengan 4 agen:
- Agent 1: Research Engine (Qwen)
- Agent 2: Dialogue Scriptwriter (Agnes AI)
- Agent 3: Audio Engine (ElevenLabs + FFmpeg)
- Agent 4: Metadata & Distribution

## Tech Stack

| Komponen | Teknologi | Cost |
|----------|-----------|------|
| Backend | Python FastAPI | Free |
| Deployment | Vercel | Free |
| Async Queue | Inngest | Free |
| Database | Supabase PostgreSQL | Free |
| File Storage | Supabase Storage | Free |
| Agent Framework | CrewAI | Free |
| LLM (Research) | Qwen API | Free/cheap |
| LLM (Script) | Agnes AI | Free/cheap |
| TTS | ElevenLabs | Free tier |
| Audio | FFmpeg | Free |
| Frontend | Jinja2 + HTMX + Tailwind | Free |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        VERCEL (Free)                             │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI endpoints                                               │
│  Jinja2 + HTMX dashboard                                        │
│  Static files (Tailwind CSS)                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Event
┌─────────────────────────────────────────────────────────────────┐
│                        INNGEST (Free)                            │
├─────────────────────────────────────────────────────────────────┤
│  Agent 1: Research (Qwen)        - 1-2 menit                   │
│  Agent 2: Scriptwriter (Agnes)   - 1-2 menit                   │
│  Agent 3: Audio (ElevenLabs)     - 5-10 menit                  │
│  Agent 4: Distribution           - 30 detik                    │
│  ✅ Parallel processing, auto-retry, no timeout                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SUPABASE (Free)                           │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL: episodes, channels, agent_tasks                    │
│  Storage: audio files                                           │
│  Realtime: live dashboard updates                               │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema

```sql
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
```

## API Endpoints

- `GET /api/episodes` - List all episodes
- `POST /api/episodes` - Create new episode
- `GET /api/episodes/{id}` - Get episode detail
- `DELETE /api/episodes/{id}` - Delete episode
- `GET /api/channels` - List all channels
- `POST /api/channels` - Create new channel
- `POST /api/pipeline/start/{episode_id}` - Start production
- `GET /api/pipeline/status/{episode_id}` - Get status

## Pipeline Flow

```
User Input (Topic)
    │
    ▼
POST /api/episodes → Create episode (status: pending)
    │
    ▼
Inngest Event: episode.created
    │
    ├──► Agent 1 (Research) → Qwen API → Research output
    │
    ├──► Agent 2 (Scriptwriter) → Agnes AI → JSON script
    │
    ├──► Agent 3 (Audio) → ElevenLabs → FFmpeg → Audio file
    │
    └──► Agent 4 (Distribution) → SEO metadata + RSS
    │
    ▼
Status: completed → Dashboard auto-update via Supabase Realtime
```

## Token Cost Estimate

| Komponen | Cost per Episode |
|----------|-----------------|
| Qwen (Research) | ~$0.001 |
| Agnes AI (Script) | ~$0.001 |
| ElevenLabs (Audio) | ~$0.10-0.20 |
| **TOTAL** | **~$0.10-0.20** |

## Environment Variables

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
ELEVENLABS_API_KEY=your_elevenlabs_key
QWEN_API_KEY=your_qwen_key
AGNES_API_KEY=your_agnes_key
INNGEST_EVENT_KEY=your_inngest_key
INNGEST_SIGNING_KEY=your_inngest_signing_key
```
