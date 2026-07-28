# 🎙️ PodFlow AI

<div align="center">

**An AI-powered end-to-end podcast production pipeline**

Generate a complete podcast from a single topic—from research and scriptwriting to AI voice synthesis, video generation, caption generation, and automatic TikTok publishing.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# 📖 Overview

PodFlow AI is an AI-powered podcast production pipeline that automates the entire content creation workflow.

Starting from a single topic, the system can:

- 🔍 Research a topic using AI
- ✍️ Generate a podcast script
- 🤖 Generate a TikTok caption
- 🎤 Convert the script into speech
- 🎬 Render a subtitle video
- 📱 Automatically upload the final video to TikTok Studio

The goal is to reduce the manual effort required to transform an idea into a ready-to-publish short-form podcast.

---

# ✨ Features

- 🔍 AI-powered topic research
- ✍️ AI podcast script generation
- 🤖 AI-generated TikTok captions
- 🎤 AI voice synthesis using ElevenLabs
- 🎬 Automatic video rendering using FFmpeg
- 🖼 Dynamic subtitle and image composition
- 📱 Automated TikTok Studio upload using Playwright
- ⚡ Background task processing with Celery
- 🗄 Supabase integration

---

# 🏗 Architecture

```
                    User Topic
                         │
                         ▼
              ┌────────────────────┐
              │ Research Agent     │
              └────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Script Agent       │
              └────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Caption Generator  │
              └────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ ElevenLabs TTS     │
              └────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Video Generator    │
              │ FFmpeg + Pillow    │
              └────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ TikTok Automation  │
              │ Playwright         │
              └────────────────────┘
```

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- Celery
- Redis / Memurai

## AI

- CrewAI
- Qwen
- Agnes AI
- ElevenLabs

## Media Processing

- FFmpeg
- Pillow

## Automation

- Playwright
- Chromium

## Database

- Supabase

---

# 📂 Project Structure

```
app/
│
├── agents/          # AI agents
├── api/             # FastAPI routes
├── auth/            # TikTok authentication
├── services/        # Business logic
├── utils/           # Shared utilities
├── video_files/     # Generated videos
├── rss_files/       # RSS feeds
│
└── main.py

scripts/
└── tiktok_uploader.py
```

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/dachi01-afk/PodFlow-Ai.git

cd PodFlow-Ai
```

## Create a virtual environment

```bash
python -m venv .venv
```

## Activate the environment

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Python dependencies

```bash
pip install -r requirements.txt
```

## Install Playwright

```bash
playwright install chromium
```

## Install FFmpeg

Make sure FFmpeg is installed and available in your system PATH.

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
SUPABASE_URL=

SUPABASE_KEY=

QWEN_API_KEY=

AGNES_API_KEY=

ELEVENLABS_API_KEY=

OPENROUTER_API_KEY=

REDIS_URL=
```

---

# 📱 TikTok Automation Setup

PodFlow AI uploads videos using Playwright and an authenticated TikTok session.

## Step 1 — Export TikTok Cookies

Export your TikTok cookies after logging into TikTok Studio.

Save them as:

```
app/auth/www_tiktok_com_cookies.json
```

A template file is included:

```
app/auth/www_tiktok_com_cookies_example.json
```

## Step 2 — Keep Credentials Private

The following files should **never** be committed:

- `.env`
- `app/auth/www_tiktok_com_cookies.json`
- `app/auth/chrome_profile/`

These files are already ignored by Git.

---

# ▶️ Running the Project

Start Redis (or Memurai).

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Start the Celery worker:

```bash
celery -A app.celery_app worker --pool=solo -l info
```

Open the frontend and begin generating podcast episodes.

---

# 🔄 Workflow

```
Generate Topic
      │
      ▼
Research
      │
      ▼
Podcast Script
      │
      ▼
TikTok Caption
      │
      ▼
Voice Generation
      │
      ▼
Video Rendering
      │
      ▼
TikTok Upload
```

---

# 🌐 API

Main endpoints:

```
POST /api/pipeline/research
POST /api/pipeline/script
POST /api/pipeline/audio
POST /api/pipeline/video
POST /api/pipeline/upload/{episode_id}
```

---

# 📸 Screenshots

## Dashboard

Coming soon.

---

## Generated Video

Coming soon.

---

## TikTok Upload Automation

Coming soon.

---

# 🛣️ Roadmap

## Completed

- ✅ AI topic research
- ✅ AI podcast script generation
- ✅ AI-generated TikTok captions
- ✅ ElevenLabs voice generation
- ✅ Automatic video rendering
- ✅ Automated TikTok Studio upload

## Planned

- [ ] AI-generated hashtags
- [ ] Multi-platform publishing
- [ ] YouTube Shorts support
- [ ] Instagram Reels support
- [ ] Spotify publishing
- [ ] Automatic scheduling
- [ ] Analytics dashboard

---

# 🔒 Security

This project requires authenticated credentials for TikTok automation.

Never commit:

- `.env`
- API keys
- Browser profiles
- TikTok cookies containing real credentials

A cookie template is included for reference.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

For significant feature additions or architectural changes, please open an issue first.

---

# 📜 License

This project is licensed under the MIT License.
