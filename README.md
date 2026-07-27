# PodFlow AI - Autonomous Podcast Network

Sistem produksi podcast otonom yang menggunakan multi-agent AI untuk riset, menulis naskah, menghasilkan audio, dan membuat metadata secara otomatis.

## Fitur Utama

- **Riset Otonom** - AI menganalisis topik trending dan menghasilkan insight terstruktur
- **Penulisan Naskah** - Dual-host personality (formal + casual) dengan dialog natural
- **Produksi Audio** - Text-to-Speech dengan gTTS dan penggabungan audio via FFmpeg
- **Metadata & SEO** - Judul, deskripsi, tags, dan konten media sosial otomatis
- **Dashboard Real-time** - Monitoring progres pipeline via CLI

## Arsitektur

```
main.py
    |
    v
PipelineOrchestrator
    |
    +---> ResearchAgent (Qwen via Groq API)
    |         |
    |         v
    +---> ScriptAgent (Agnes AI API)
    |         |
    |         v
    +---> AudioAgent (gTTS + FFmpeg)
    |         |
    |         v
    +---> MetadataAgent (SEO + Social Content)
              |
              v
        output/
        +-- audio/podcast.mp3
        +-- metadata/metadata_*.json
        +-- social/social_content_*.json
```

## Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Research Agent | Qwen 3.6 27B via Groq API |
| Script Agent | Agnes 2.0 Flash via Agnes AI API |
| Audio Engine | gTTS + pydub + FFmpeg |
| CLI Dashboard | Rich |
| Bahasa | Python 3.12 |

## Persiapan

### 1. Clone Repository

```bash
git clone https://github.com/username/podflow-ai.git
cd podflow-ai
```

### 2. Buat Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download dari https://ffmpeg.org/download.html
```

### 5. Setup API Keys

Copy `.env.example` ke `.env` dan isi API keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_key=gsk_xxxxxxxxxxxxxxxx
AGNES_API_KEY=sk_xxxxxxxxxxxxxxxx
```

**Cara mendapatkan API keys:**

- **Groq** (untuk Qwen): Daftar gratis di [console.groq.com](https://console.groq.com)
- **Agnes AI**: Daftar gratis di [platform.agnes-ai.com](https://platform.agnes-ai.com)

## Cara Penggunaan

### Jalankan Pipeline

```bash
python main.py
```

### Pilih Topik

```
PODFLOW AI - Select Topic

Available trending topics:
  1. Strategi Keuangan Mikro untuk Usaha Kecil
  2. Tips Productivity Kerja dari Rumah
  3. Tren Teknologi AI di Indonesia 2026

  Or enter your own topic below:

Your choice (1-3 or custom topic):
```

Masukkan angka (1-3) atau ketik topik custom, lalu tekan Enter.

### Output

Pipeline akan menghasilkan file di folder `output/`:

```
output/
+-- audio/
|   +-- podcast.mp3          # File audio podcast
+-- metadata/
|   +-- metadata_*.json      # SEO metadata
+-- social/
    +-- social_content_*.json # Konten media sosial
```

### Contoh Output

**metadata.json:**
```json
{
  "title": "KUR 2024 & Pinjol: Gak Perlu Takut, Ini Rahasianya! | PodFlow AI",
  "description": "Podcast tentang strategi keuangan mikro...\n\nTopik: Strategi Keuangan Mikro\n\nDiproduksi oleh PodFlow AI",
  "tags": ["strategi keuangan mikro", "podcast", "indonesia", "ai"],
  "duration": "1-2 minutes",
  "created_at": "2026-07-27T22:47:40"
}
```

**social_content.json:**
```json
{
  "show_notes": "## KUR 2024 & Pinjol...\n\nDeskripsi podcast...",
  "x_thread": [
    "Pod baru aja rilis: KUR 2024 & Pinjol...",
    "1/ Deskripsi podcast...",
    "2/ Dengarkan sekarang di PodFlow AI!"
  ],
  "linkedin_post": "New Episode: KUR 2024 & Pinjol..."
}
```

## Struktur Proyek

```
podflow-ai/
+-- main.py                 # Entry point
+-- config.py               # Konfigurasi API keys & model
+-- requirements.txt        # Python dependencies
+-- .env.example            # Template API keys
+-- agents/
|   +-- research_agent.py   # Riset via Qwen/Groq
|   +-- script_agent.py     # Penulisan naskah via Agnes AI
|   +-- audio_agent.py      # Produksi audio (gTTS + FFmpeg)
|   +-- metadata_agent.py   # SEO & konten media sosial
+-- pipeline/
|   +-- orchestrator.py     # Pipeline orchestrator
+-- dashboard/
|   +-- cli_dashboard.py    # Dashboard real-time
+-- utils/
|   +-- json_utils.py       # JSON extraction dari LLM output
|   +-- audio_utils.py      # Utility audio processing
+-- data/
|   +-- trending_topics.json # Database topik trending
+-- docs/
    +-- prompt_architecture.md # Dokumentasi prompt
    +-- pitch_deck.md         # Business pitch
```

## Prompt Architecture

### Research Agent

Menggunakan Qwen 3.6 27B via Groq untuk menganalisis topik:

- Output: JSON dengan key_facts, sentiment, trending_angles, sources
- Fokus: Konteks lokal Indonesia, data 7 hari terakhir
- Filter: Hoaxes dan misinformasi

### Script Writer

Menggunakan Agnes 2.0 Flash untuk menulis naskah podcast:

- Host A: Formal expert, Bahasa Indonesia baku
- Host B: Casual skeptic, bahasa gaul Indonesia
- Gaya: Percakapan natural seperti teman ngobrol
- Durasi: 1-2 menit (200-300 kata)

### Audio Engine

Menggunakan gTTS dan FFmpeg untuk produksi audio:

- Text-to-Speech: gTTS dengan bahasa Indonesia
- Penggabungan: pydub + FFmpeg
- Output: MP3 192kbps

### Metadata Engine

Menghasilkan konten SEO dan media sosial:

- Metadata: Judul, deskripsi, tags, durasi
- Social: Show notes, Twitter thread, LinkedIn post

## Biaya API

| Model | Provider | Input/1M tokens | Output/1M tokens |
|-------|----------|-----------------|------------------|
| Qwen 3.6 27B | Groq | $0.60 | $3.00 |
| Agnes 2.0 Flash | Agnes AI | Gratis | Gratis |

**Estimasi biaya per episode:** ~$0.01-0.05 (tergantung panjang naskah)

## Troubleshooting

### Error: GROQ_API_KEY not found
- Pastikan file `.env` sudah dibuat
- Pastikan API key sudah benar

### Error: Unknown request URL
- Pastikan `GROQ_BASE_URL = "https://api.groq.com"` (tanpa `/openai/v1`)

### Error: No complete JSON object found
- Model mengembalikan output yang terpotong
- Coba jalankan ulang pipeline

### Error: ffmpeg not found
- Install FFmpeg: `sudo apt install ffmpeg` (Ubuntu/Debian)

### Audio tidak terdengar
- Pastikan file `output/audio/podcast.mp3` ada
- Coba buka dengan media player lain

## Lisensi

MIT License - Untuk keperluan hackathon dan pengembangan lebih lanjut.

## Kontak

Untuk pertanyaan atau kontribusi, silakan buka issue di GitHub repository.
