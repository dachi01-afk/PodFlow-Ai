# 🎙️ PodFlow AI

<div align="center">

**An AI-powered end-to-end podcast production pipeline**

Generate a complete podcast from a single topic—from research and scriptwriting to AI voice synthesis, video generation, caption generation, and automatic TikTok publishing.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# 📖 Overview

PodFlow AI is an AI-powered podcast production pipeline that automates the entire content creation workflow.

Starting from a single topic, the system performs:

- Topic research
- Podcast script generation
- TikTok caption generation
- AI voice synthesis
- Video rendering
- Automatic TikTok upload

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
├── agents/            # AI agents
├── api/               # FastAPI endpoints
├── auth/              # TikTok authentication
├── services/          # Business logic
├── utils/             # Shared utilities
├── video_files/       # Generated videos
├── rss_files/         # RSS data
│
├── main.py
│
scripts/
└── tiktok_uploader.py
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/PodFlow-AI.git

cd PodFlow-AI
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browsers

```bash
playwright install
```

---

# ⚙ Environment Variables

Create a `.env` file.

```env
SUPABASE_URL=

SUPABASE_KEY=

QWEN_API_KEY=

AGNES_API_KEY=

ELEVENLABS_API_KEY=

REDIS_URL=

OPENROUTER_API_KEY=
```

---

# 📱 TikTok Automation Setup

PodFlow AI uploads videos using Playwright and a valid TikTok authentication session.

## 1. Export your TikTok cookies

Export your authenticated TikTok cookies and save them as:

```
app/auth/www_tiktok_com_cookies.json
```

A template is provided:

```
app/auth/www_tiktok_com_cookies_example.json
```

## 2. Keep authentication private

The following files should **never** be committed:

- `.env`
- `app/auth/www_tiktok_com_cookies.json`
- `app/auth/chrome_profile/`

These files are already included in `.gitignore`.

---

# ▶ Running

Start Redis (or Memurai).

Start FastAPI

```bash
uvicorn app.main:app --reload
```

Start Celery

```bash
celery -A app.celery_app worker --pool=solo -l info
```

Open the frontend and start generating podcast episodes.

---

# 🔄 Workflow

Current production workflow

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

Main endpoints include:

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

# 🛣 Roadmap

- [x] AI topic research
- [x] AI podcast script generation
- [x] AI-generated TikTok captions
- [x] ElevenLabs voice generation
- [x] Automatic video rendering
- [x] Automated TikTok Studio upload

Future improvements

- [ ] AI-generated hashtags
- [ ] Multi-platform publishing
- [ ] YouTube Shorts support
- [ ] Instagram Reels support
- [ ] Automatic scheduling
- [ ] Analytics dashboard
- [ ] Spotify publishing

---

# 🔒 Security

This project requires authentication for TikTok automation.

Never commit:

- `.env`
- TikTok cookie files containing real credentials
- Browser profiles
- API keys

Use the provided cookie template file as a reference when setting up a new environment.

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

Please open an issue before submitting large feature changes.

---

# 📜 License

This project is licensed under the MIT License.
