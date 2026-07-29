"""
PodFlow AI - Agent: TikTok Caption Generator
Menggunakan Agnes AI untuk membuat caption TikTok.
"""

import httpx
from config import get_settings

settings = get_settings()


def generate_tiktok_caption(topic: str, script: list) -> str:
    """Generate TikTok caption using Agnes AI"""

    transcript = "\n".join(
        dialogue["text"]
        for dialogue in script
    )

    prompt = f"""
Anda adalah AI Social Media Strategist untuk PodFlow AI.

Buat caption TikTok berdasarkan podcast berikut.

Topik:
{topic}

Transkrip Podcast:
{transcript}

Tujuan:
- Menarik perhatian pengguna dalam beberapa detik pertama.
- Membuat audiens penasaran untuk menonton video.
- Meningkatkan engagement.
- Tetap sesuai dengan isi podcast.

Aturan:
- Gunakan Bahasa Indonesia.
- Maksimal 180 karakter.
- Mulai dengan hook yang menarik.
- Jangan mengulang isi podcast secara penuh.
- Hindari clickbait yang menyesatkan.
- Tambahkan emoji secukupnya.
- Sertakan Call-To-Action yang natural.
- Tambahkan 5–8 hashtag yang relevan.

Output HANYA berupa caption TikTok.
"""

    response = httpx.post(
        f"{settings.agnes_api_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.agnes_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "agnes-2.0-flash",
            "messages": [
                {
                    "role": "system",
                    "content": """
Anda adalah AI Social Media Strategist untuk PodFlow AI.

Tugas Anda adalah membuat caption TikTok yang menarik berdasarkan isi podcast.

Target Audiens:
- Mahasiswa
- Fresh graduate
- Content creator
- Pelaku UMKM usia 18–30 tahun.

Aturan:
- Gunakan Bahasa Indonesia.
- Caption harus singkat, menarik, dan mudah dibaca.
- Kalimat pertama harus menjadi hook.
- Hindari clickbait yang menyesatkan.
- Sertakan Call-To-Action yang natural.
- Tambahkan hashtag yang relevan.
- Output hanya berupa caption tanpa penjelasan tambahan.
""",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.8,
            "max_tokens": 300,
        },
        timeout=120.0,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()