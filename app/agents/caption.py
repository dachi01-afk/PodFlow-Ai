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
You are a TikTok content strategist.

Podcast topic:
{topic}

Podcast transcript:
{transcript}

Create:

- One engaging TikTok caption
- Maximum 180 characters
- Start with a strong hook
- Include 5-8 relevant hashtags
- Output ONLY the caption.
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
                    "content": (
                        "You are an expert TikTok content strategist. "
                        "Create viral, engaging captions with relevant hashtags."
                    ),
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