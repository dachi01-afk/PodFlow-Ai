"""
PodFlow AI - Agent 1: Research Engine
Menggunakan Qwen API untuk riset topik podcast.
"""

import httpx
import json
import re
from config import get_settings

settings = get_settings()


def research_topic(topic: str) -> dict:
    """Research a topic using Qwen API"""

    prompt = f"""
Anda adalah AI Research Agent untuk PodFlow AI.

Lakukan riset mendalam mengenai topik berikut:

Topik: {topic}

Tujuan:
- Mengumpulkan informasi terbaru dari sumber yang terpercaya dan relevan.
- Mengidentifikasi tren terkini dan fakta penting mengenai topik.
- Menjelaskan topik menggunakan Bahasa Indonesia yang sederhana, jelas, dan mudah dipahami.
- Menghindari opini pribadi, spekulasi, atau informasi yang tidak memiliki dasar.

Struktur output harus berupa JSON:

{{
    "topic": "{topic}",
    "summary": "Ringkasan topik dalam 2-3 kalimat",
    "key_facts": ["fakta 1", "fakta 2", "fakta 3", "fakta 4", "fakta 5"],
    "trends": ["tren 1", "tren 2", "tren 3"],
    "sentiment": "positif/negatif/netral",
    "sources": ["sumber 1", "sumber 2"]
}}

Aturan:
- Berikan minimal 5 fakta penting.
- Berikan minimal 3 tren terbaru.
- Gunakan sumber yang terpercaya apabila memungkinkan.
- Pastikan output berupa JSON yang valid.
- Jangan memberikan penjelasan tambahan di luar JSON.
"""

    response = httpx.post(
        f"{settings.qwen_api_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.qwen_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen/qwen3.6-27b",
            "messages": [
                {
                    "role": "system",
                    "content": """
Anda adalah AI Research Agent untuk PodFlow AI.

Tugas Anda adalah melakukan riset mendalam berdasarkan topik yang diberikan sebagai dasar pembuatan podcast edukatif.

Tujuan:
- Mengumpulkan informasi terbaru dari sumber yang terpercaya dan relevan.
- Mengidentifikasi tren dan fakta penting dari topik yang dibahas.
- Menjelaskan topik menggunakan Bahasa Indonesia yang sederhana, jelas, dan mudah dipahami.
- Menghindari opini pribadi, spekulasi, atau informasi yang tidak memiliki dasar.

Aturan:
- Prioritaskan informasi terbaru apabila tersedia.
- Gunakan data atau statistik yang relevan jika memungkinkan.
- Hindari pengulangan informasi.
- Pastikan seluruh output menggunakan Bahasa Indonesia.
- Selalu mengikuti format JSON yang diminta oleh pengguna.
- Jangan memberikan markdown atau penjelasan di luar JSON.
""",
                },
                {"role": "user", "content": prompt + "\n\n/no_think"},
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
        },
        timeout=120.0,
    )

    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"]

    content = re.sub(r"<think>[\s\S]*?</think>", "", content).strip()

    json_match = re.search(r"\{[\s\S]*\}", content)
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