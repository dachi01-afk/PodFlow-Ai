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
Anda adalah peneliti ahli. Teliti topik berikut dan berikan hasilnya dalam format JSON:

Topik: {topic}

Struktur output harus berupa JSON:
{{
    "topic": "{topic}",
    "summary": "Ringkasan topik dalam 2-3 kalimat",
    "key_facts": ["fakta 1", "fakta 2", "fakta 3", "fakta 4", "fakta 5"],
    "trends": ["tren 1", "tren 2", "tren 3"],
    "sentiment": "positif/negatif/netral",
    "sources": ["sumber 1", "sumber 2"]
}}

Berikan minimal 5 fakta kunci dan 3 tren.
Pastikan output berupa JSON yang valid.
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
                    "content": "Anda adalah peneliti ahli yang menghasilkan riset berkualitas tinggi dalam format JSON.",
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
