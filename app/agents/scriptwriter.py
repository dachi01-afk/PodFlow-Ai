"""
PodFlow AI - Agent 2: Dialogue Scriptwriter
Menggunakan Agnes AI untuk menulis dialog podcast.
"""

import httpx
import json
import re
from config import get_settings

settings = get_settings()


def generate_script(topic: str, research: dict) -> list:
    """Generate dialogue script using Agnes AI"""

    prompt = f"""
Anda adalah AI Dialogue Scriptwriter untuk PodFlow AI.

Buat dialog podcast berdasarkan hasil riset berikut.

Topik:
{topic}

Hasil Riset:
{json.dumps(research, ensure_ascii=False)}

Buat dialog antara 2 host:

Host_A
- Berperan sebagai pakar teknologi.
- Menjelaskan menggunakan fakta dari hasil riset.
- Profesional, tenang, dan mudah dipahami.
- Memberikan contoh sederhana jika diperlukan.

Host_B
- Berperan sebagai pendengar yang penasaran.
- Aktif bertanya.
- Mewakili rasa penasaran audiens.
- Memberikan tanggapan secara natural.

Aturan:
- Gunakan Bahasa Indonesia sehari-hari.
- Percakapan harus terasa natural seperti podcast sungguhan.
- Jangan terdengar seperti membaca artikel.
- Pastikan kedua host saling merespon.
- Gunakan sedikit humor yang natural.
- Jangan mengulang informasi yang sama.
- Gunakan hasil riset sebagai sumber utama pembahasan.
- Akhiri percakapan dengan penutup yang singkat.

Format output HARUS berupa JSON array:

[
    {{
        "speaker": "Host_A atau Host_B",
        "emotion": "enthusiastic/confused/neutral/thinking/excited",
        "pause_duration": 0.5,
        "text": "Teks dialog"
    }}
]

Buat minimal 6 dialog.

Pastikan output berupa JSON array yang valid.

Jangan memberikan markdown ataupun penjelasan tambahan.
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
Anda adalah AI Dialogue Scriptwriter untuk PodFlow AI.

Tugas Anda adalah mengubah hasil riset menjadi dialog podcast edukatif yang menarik.

Gaya podcast:
- Edukatif
- Santai
- Interaktif
- Mudah dipahami
- Menggunakan Bahasa Indonesia.

Target audiens:
- Mahasiswa
- Fresh graduate
- Content creator
- Pelaku UMKM usia 18–30 tahun.

Aturan:
- Dialog harus natural.
- Gunakan Bahasa Indonesia sehari-hari.
- Hindari paragraf yang terlalu panjang.
- Pastikan kedua host aktif berbicara.
- Jelaskan istilah teknis dengan sederhana.
- Selalu ikuti format JSON yang diminta pengguna.
- Jangan memberikan markdown atau penjelasan di luar JSON.
""",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
            "max_tokens": 3000,
        },
        timeout=120.0,
    )

    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"]

    json_match = re.search(r"\[[\s\S]*\]", content)
    if json_match:
        return json.loads(json_match.group())

    return [
        {
            "speaker": "Host_A",
            "emotion": "neutral",
            "pause_duration": 1.0,
            "text": f"Selamat datang di podcast kita. Hari ini kita akan membahas tentang {topic}.",
        },
        {
            "speaker": "Host_B",
            "emotion": "confused",
            "pause_duration": 0.5,
            "text": "Wah, menarik sekali. Aku sering dengar tentang topik ini, tapi sebenarnya apa sih maksudnya?",
        },
    ]