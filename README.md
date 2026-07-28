# PodFlow AI - Developer Documentation

## System Overview

PodFlow AI adalah sistem AI otonom untuk produksi podcast end-to-end dengan 4 agen:
- **Agent 1: Research Engine** (Qwen API)
- **Agent 2: Scriptwriter** (Agnes AI)
- **Agent 3: Audio Engine** (ElevenLabs + FFmpeg)
- **Agent 4: Distribution** (SEO + RSS)

Ini menggunakan FastAPI dengan frontend yang dibangkit dinamis menggunakan Jinja2 + HTMX + Tailwind CSS untuk dashboard yang terhubung secara real-time.

## 🏃‍♂️ Cara Cepat Instalasi (Windows, macOS, Linux)

### Prerequisites

```bash
# Python 3.9 atau lebih baru
# PostgreSQL (diaktifkan pada Supabase)
# Package manager sistem operasi
```

### 1. Clone Repository

```bash
# Windows (PowerShell)
git clone https://github.com/yourusername/podflow-ai.git

# macOS/Linux
cd /path/to/
git clone https://github.com/yourusername/podflow-ai.git

# Git worktree (di rekomendasikan)
git worktree add podflow-ai production
```

### 2. Setup Lingkungan Python Virtual

#### Windows (PowerShell/Prompt)

```powershell
# Buat lingkungan virtual
py -3 -m venv venv

# Aktifkan
venv\Scripts\Activate.ps1

# Pada Windows PowerShell baru
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS/Linux

```bash
# Buat lingkungan virtual
touch requirements.txt  # Buat placeholder file untuk testing

# Activate saat Anda membutuhkannya
mkdir -p venv && python3 -m venv venv
echo "source venv/bin/activate" >> ~/.bashrc
virtenv
```

#### Menggunakan Git Worktree

```bash
# Buka terminal baru di worktree
git worktree list
cd /absolute/path/to/podflow-ai
```

### 3. Instal Dependensi Python

```bash
# Install dependensi dari requirements.txt
pip install -r requirements.txt

# Jika Anda menggunakan Poetry (di rekomendasikan)
poetry install

# Untuk development (ditambah dependensi dev tools)
poetry install --with dev
```

### 4. Setup .env File

Salin template dari `.env.example` ke `.env` dan sesuaikan nilai-nilai-nya:

```bash
# Linux/macOS
cp .env.example .env

# Windows
copy .env.example .env
```

Edit `.env` dengan API keys yang relevan:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# ElevenLabs
ELEVENLABS_API_KEY=your_elevenlabs_key

# Qwen (via Groq)
QWEN_API_KEY=your_qwen_key

# Agnes AI
AGNES_API_KEY=your_agnes_key

# Redis (untuk Celery)
REDIS_URL=redis://localhost:6379/0

# Inngest (untuk async pipelines)
INNGEST_EVENT_KEY=your_inngest_event_key
INNGEST_SIGNING_KEY=your_inngest_signing_key
```

### 5. Setup Supabase

#### Opsi 1: Gunakan Supabase Cloud Free Tier (direkomendasikan)

1. Kunjungi https://supabase.io
2. Buat proyek baru
3. Upload SQL schema

#### Opsi 2: Setup Lokal dengan Docker

```bash
# Pull docker-compose
docker-compose up -d

# Atau gunakan Supabase CLI
docker run --name supabase -p 5432:5432 -p 8000:8000 supabase/supa basedb bash

# Buat database dan tabel
sql-editor
git add scripts/setup_database.py
```

### 6. Setup Redis

#### Linux/macOS (berbasis package manager)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# macOS (brew)
brew install redis

# Mulai redis (default dengan sistem)
sudo systemctl enable redis
sudo systemctl start redis
```

#### Windows

```powershell
# Install dari chocolatey
choco install redis-32-bit

# Atau unduh installer dari https://redis.io/download

# Pada Windows dengan Chocolatey:
sudo net start Redis
```

#### Docker

```bash
docker run -d -p 6379:6379 --name redis redis:latest
docker ps
```

### 7. setup FFmpeg

#### Linux/macOS

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS (brew)
brew install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

#### Windows

```powershell
# Unduh dari https://ffmpeg.org/download-static/
# Atau install dengan chocolatey
choco install ffmpeg
```

### 8. Jalankan Aplikasi

#### Local Development

```bash
# Uji API
python main.py

# Pada terminal terpisah (untuk Celery)
celery -A celery_app worker -l info

# Pada terminal terpisah (untuk ngrok - untuk akses eksternal)
npm install -g ngrok
ngrok http 8000
```

#### Production dengan Docker

```bash
# Build image
docker build -t podflow-ai .

# Jalankan container
docker run -d -p 8000:8000 \
  -e SUPABASE_URL=\"your-supabase-url\" \
  -e SUPABASE_KEY=\"your-supabase-key\" \
  podflow-ai
```

#### Production dengan Docker Compose

```yaml
docker-compose.yml
docker-compose up -d
```

### 9. Jalankan Backend Development (Hot Reload)

```bash
# Menggunakan Python FastAPI dengan hot reload
# Pada terminal 1
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Pada terminal 2 (celery worker)
celery -A celery_app worker -l info

# Pada terminal 3 (untuk ngrok)
ngrok http 8000
```

### 10. Jalankan Frontend Development dengan Hot Reload

```bash
# Karena frontend menggunakan HTML statis + HTMX, tidak memerlukan build secara mandiri
# Layanan statis disertakan dalam FastAPI dengan `StaticFiles`

# Jika Anda ingin menjalankan frontend secara independen:
# Install package global
npm install -g http-server

# Jalankan dari direktori static
http-server static -p 3000
```

## 🛠 Konfigurasi & Pengembangan Lebih Lanjut

### File Konfigurasi Tambahan

#### `config.py`
```python
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # ElevenLabs
    ELEVENLABS_API_KEY: str
    
    # Qwen (Groq)
    QWEN_API_KEY: str
    QWEN_API_URL: str = "https://api.groq.com/openai/v1"
    
    # Agnes AI
    AGNES_API_KEY: str
    AGNES_API_URL: str = "https://api.agnes.ai/v1"
    
    # Celery/Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # Inngest
    INNGEST_EVENT_KEY: str
    INNGEST_SIGNING_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

#### `.env.example`
```bash
# Template file dengan placeholder
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=placeholder-key
ELEVENLABS_API_KEY=placeholder-key
QWEN_API_KEY=placeholder-key
AGNES_API_KEY=placeholder-key
INNGEST_EVENT_KEY=placeholder-key
INNGEST_SIGNING_KEY=placeholder-key
REDIS_URL=redis://localhost:6379/0
```

### Konfigurasi Tingkat Lanjut

#### Custom Prompt Templates untuk Agen

```python
# app/prompts/research_agent.py
RESEARCH_PROMPT = """
Anda adalah peneliti AI yang mencari tren terkini. Untuk topik yang diberikan:

1. Cari setidaknya 3-5 sumber yang kredibel dan terkini
2. Ekstrak fakta kunci (angka, tanggal, kutipan)
3. Diberikan sentimen (positif/negatif/netral) dari setiap sumber
4. Tulis ringkasan dalam 150-200 kata yang mencakup:
   - Apa trennya
   - Mengapa itu penting
   - Perspektif yang saling bertentangan (jika ada)
   - Implikasi masa depan
5. Output harus berupa JSON yang dapat diparsing dengan format berikut:
   {
     "topic": "...",
     "summary": "...",
     "key_facts": [...],
     "sentiment": "...",
     "sources": [...]
   }
"""

# app/prompts/scriptwriter_agent.py
SCRIPTWRITER_PROMPT = """
Anda adalah penulis skenario profesional dan pencipta dialog untuk podcast . Untuk topik yang diberikan dan penelitian yang tersedia:

1. Tentukan persona yang tepat untuk dua host berdasarkan topik
2. Tulis dialog yang natural, autentik dan seimbang
3. Sertakan petunjuk emosi yang spesifik (misalnya bersemangat, bingung, berpikir) untuk setiap bagian dialog
4. Sertakan jeda untuk transisi (dalam milidetik) untuk kemajuan ritme alami
5. Setiap bagian dialog harus memiliki minimal satu hook emosional yang kuat dan energi yang mengalir
6. Sertakan konteks latar belakang singkat sebagai bagian dari bagian dialog untuk membangun kepribadian karakter

Output harus berupa file JSON yang dapat diparsing dengan format berikut:
{
  "topic": "...",
  "host_a_personality": "...",
  "host_b_personality": "...",
  "dialogues": [
    {
      "speaker": "Host_A",
      "emotion": "...",
      "text": "...",
      "pause_duration": ...,
      "context_background": "..."
    }
  ]
}
"""
```

#### Jalankan Uji Coba Sistem dan Autentikasi

```bash
# Jalankan suite uji lengkap
pytest tests/ -v --cov=app --cov-report=html

# Uji integrasi E2E
playwright test

# Uji komponen backend secara mandiri
pytest tests/unit/test_episodes.py -v
pytest tests/unit/test_agents.py -v
```

### Mode Pengembangan Lanjutan

#### Mode Debug Otomatis

```bash
# Mode debug dengan sampel data
touch .env.example
# Isi dengan sampel kunci untuk testing
```

#### Lokalisasi (untuk pengembangan di luar AS)

```python
# app/utils/translation.py
TRANSLATIONS = {
    "id": {
        "navigation": {
            "dashboard": "Dashboard",
            "channels": "Channels",
            "new_episode": "+ New Episode"
        }
    },
    "en": {
        "navigation": {
            "dashboard": "Dashboard",
            "channels": "Channels",
            "new_episode": "+ New Episode"
        }
    }
}
```

## 🧪 Pengujian Komponen

### Jalankan Semua Uji

```bash
# Uji unit (tercepat)
pytest tests/unit/ -v

# Uji integrasi
pytest tests/integration/ -v

# Uji E2E (browser)
playwright test

# Laporan cakupan
pytest --cov=app --cov-report=term-missing
```

### Struktur Uji Coba

```bash
tests/
├── unit/                    # Uji komponen Python individu
│   ├── test_episodes.py     # Uji API endpoints
│   ├── test_agents.py       # Uji logika agen AI
│   └── test_utils.py        # Uji utilitas internal
├── integration/            # Uji API endpoints terintegrasi
│   ├── test_api_client.py  # HTTP client tests
│   └── test_supabase.py    # Supabase integration tests
├── e2e/                     # Uji full end-to-end
│   ├── pages/              # File page object
│   ├── fixtures/           # Config untuk test browser
│   └── tests/              # Uji implementasi Playwright
├── fixtures/               # Data untuk semua uji
└── conftest.py             # Konfigurasi global
```

## 🔧 Troubleshooting

### Masalah Umum

#### "404 Not Found: /static/css/styles.css"

```
# Masalah: Static files tidak disajikan

Solution:
1. Pastikan direktori static/ ada di root:
   ls -la static/                # Harus menampilkan css/ di sini

2. Periksa aplikasi FastAPI:
   # Edit main.py untuk mengaktifkan static files
   app.mount("/static", StaticFiles(directory="static"), name="static")

3. Restart server
```

#### "Koneksi ditolak: Tidak dapat terhubung ke Redis"

```
# Masalah: Redis tidak berjalan

Solution:
# Linux/macOS
sudo systemctl status redis
sudo systemctl start redis

# Windows (Service)
sc query Redis
# Start service jika tidak running
sc start Redis

# Atau restart
sudo systemctl restart redis

# Test koneksi di python
python3 -c "import redis; r = redis.Redis(); print(r.ping())"
```

#### "503 Service Unavailable: Supabase tidak dapat diakses"

```
# Masalah: Supabase tidak terhubung

Solution:
# Periksa .env
vi .env
# Pastikan SUPABASE_URL dan SUPABASE_KEY benar

# Test koneksi
python3 -c "
from app.core.supabase_client import get_supabase
supabase = get_supabase()
result = supabase.table('episodes').select('id').limit(1).execute()
print('Supabase terhubung:', result.data)
"
```

#### "Playwright tidak dapat menangkap screenshot"

```
# Masalah: Playwright tidak dapat akses halaman

Solution:
# Jalankan server backend
python main.py &

# Jalankan server frontend statis (jika diperlukan)
http-server static -p 8080 &

# Coba akses halaman pertama
# wget -q -O- http://localhost:8000
```

### Diagnosa Ketika Uji Gagal

```bash
# Jalankan dengan output lebih detail
pytest tests/ -v -s --tb=short

# Dapatkan detail stack
pytest tests/ --tb=long

# Jalankan ulang sekali saja
pytest tests/unit/test_episodes.py::test_list_episodes -xvs

# Debug HTTP request
curl -v http://localhost:8000/api/episodes
```

## 📚 Referensi Bermanfaat

### Pustaka Python

```bash
# Instal pustaka tambahan
pip install poetry
curl -LsSf https://box.juliangruenitz.de/python-poetry-installer | python

# Atau gunakan pipenv (alternatif)
pip install pipenv
pipenv install
```

### Pengembangan Web

#### Tailwind CSS
```bash
# CDN (untuk development)
<script src="https://cdn.tailwindcss.com"></script>

# Terinstall lokal (di rekomendasikan untuk kustomisasi)
npm install -D tailwindcss postcss autoprefixer
cd static && npx tailwindcss init -p tailwind.config.js
```

#### HTMX
```html
<!-- CDN -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

#### Live Reload
```bash
# Gunakan mksc roles.sh uvicorn
pip install hotreload
```

### Alat Produktivitas

#### Git
```bash
# Konfigurasi global
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Aliases yang berguna
git config --global alias.st "status"
git config --global alias.co "commit -m"
git config --global alias.br "branch"
git config --global alias.ff "merge --ff-only"
```

## 🚀 Deployment & hosting

### Production (Docker)

```bash
# Bangun dan jalankan
docker build -t podflow-ai .
docker run -d -p 8000:8000 podflow-ai

# Dengan compose (di rekomendasikan)
docker-compose build
docker-compose up -d
```

### Staging (GitHub Actions)

### Vercel (Frontend-only)

```bash
# Jika Anda ingin hanya frontend static
yarn add -D vercel-n3
vercel --prod
```

## 🎯 Rekomendasi Dasar untuk Lint dan Type Check

### Linting

```bash
# black (formatter)
black app/ tests/

# isort (import sorter)
isort app/ tests/

# flake8 (linting)
flake8 app/ tests/

# mypy (type checking)
mypy app/ --ignore-missing-imports
```

### Format Uji Coba

```python
# app/api/episodes_test.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_episodes_empty():
    response = client.get("/api/episodes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["episodes"] == []

def test_create_episode():
    payload = {
        "channel_id": "test-channel",
        "topic": "Test Topic"
    }
    response = client.post("/api/episodes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Test Topic"
    assert data["status"] == "pending"
    assert "id" in data
```

### Etika Komunitas

- Kode selalu terupdate. Merge segera setelah PR dibuat.
- Ketika memberikan saran pada PR, berikan detail spesifik untuk alasan perubahan.
- Ketika menemukan bug, buka issue dan berikan reproduksi steps untuk mengujinya.
- Ketika mendonate atau mengedit file lain, cantumkan sumbernya.
- Hindari duplikasi PR (seperti s3mple PR dan PR yang disatukan).
- Untuk kontribusi besar, mulailah dengan membuka issue dan diskusikan solusi sebelum kirim PR.

## 📬 Community Contribution

### Issues & Feature Requests

- Ikuti format issue yang ada (title: "[feature/request] title", "[bug] judul")
- Cantumkan reproduksi steps untuk bug
- Tambahkan label yang sesuai (bug, enhancement, documentation, etc.)

### Pull Requests

- Mulailah dengan cabang yang deskripsinya mencerminkan fitur/problem
- Lengkapi deskripsi PR dengan checklist:
  - [ ] Saya menjalankan semua linting/test yang relevan
  - [ ] Saya telah update README dengan dokumentasi yang sesuai
  - [ ] Kode saya mengikuti konvensi gaya repository
- Buka PR ke `main` (atau jika ada) branch target yang sesuai
- Periksa komentar PR dan lakukan perubahan yang diminta

### Budayanya

- Kode selalu terupdate. Merge segera setelah PR dibuat.
- Ketika memberikan saran pada PR, berikan detail spesifik untuk alasan perubahan.
- Ketika menemukan bug, buka issue dan berikan reproduksi steps untuk mengujinya.
- Ketika mendonate atau mengedit file lain, cantumkan sumbernya.
- Hindari duplikasi PR (seperti s3mple PR dan PR yang disatukan).
- Untuk kontribusi besar, mulailah dengan membuka issue dan diskusikan solusi sebelum kirim PR.

## 📚 Referensi Bermanfaat

### Penggunaan Lanjutan

#### Async Task Priority

```python
# app/tasks/pipeline.py
@celery.task(bind=True, default_retry_delay=30, max_retries=3)
def process_episode_with_priority(self, episode_id, priority="high"):
    try:
        # Process logic based on priority
        if priority == "high":
            # Process immediately
            pass
        else:
            # Queue for later
            pass
    except Exception as exc:
        self.retry(exc)
```

#### Custom Middleware

```python
# app/middleware.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request
        print(f"Request: {request.method} {request.url}")
        
        # Add custom headers
        response = await call_next(request)
        response.headers["X-Custom-Header"] = "PodFlow-AI"
        
        # Response processing
        return response
```

## 🤝 Join Our Community

- Discord: [masuk discord](https://discord.gg/podflow)
- Twitter: [@PodFlowAI](https://twitter.com/PodFlowAI)
- LinkedIn: [PodFlow AI](https://www.linkedin.com/company/podflow-ai)
- Stack Overflow: [Tag: podflow](https://stackoverflow.com/questions/tagged/podflow)

## 🎯 Tujuan Selanjutnya

- [ ] Izinkan export episode ke formato yang berbeda (JSON, Markdown, HTML)
- [ ] Tambahkan fitur kolaborasi (tim editor bersama)
- [ ] Implementasi dashboard analitik terintegrasi
- [ ] Tambahkan fitur auto-upload ke feed podcast (iTunes, Spotify, Google Podcasts)
- [ ] Integrasikan Text-to-Speech dengan ElevenLabs untuk preview audio

## 📅 Changelog

### v1.0.0 (2024-07-28)
- Feature rilis awal backend FastAPI & Celery
- Frontend dashboard HTML yang dibangkit dinamis
- Agensi AI menggunakan Qwen API & Agnes AI
- Threading episode otomatis dengan pipeline FFmpeg
- Dashboard status real-time dengan HTMX dan polling

### v0.9.0 (2024-01-28)
- Prototipe penelitian dan pembuatan naskah awal
- Integrasi awal ElevenLabs TTS
- Format RSS feed dasar
- Penyimpanan kunci di .env file

## 🎓 Lisensi

MIT License - Lihat FILE_LICENSE untuk detail.
