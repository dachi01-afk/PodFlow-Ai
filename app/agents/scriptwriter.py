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
Pastikan output berupa JSON array yang valid.
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
                    "content": "Anda adalah penulis dialog podcast profesional dengan gaya bahasa Indonesia yang natural dan humoris.",
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
            "text": f"Selamat datang di podcast kita hari ini tentang {topic}.",
        },
        {
            "speaker": "Host_B",
            "emotion": "curious",
            "pause_duration": 0.5,
            "text": "Wah, menarik sekali! Bisa ceritakan lebih lanjut?",
        },
    ]
