from typing import Dict
from app.core.supabase_client import get_supabase
from app.utils.rss import generate_rss_feed
from datetime import datetime, timezone


def generate_metadata(topic: str, script: Dict) -> Dict:
    """Generate SEO metadata for the episode"""

    title = f"PodFlow: {topic}"

    dialogues = script.get("dialogues", [])
    description_parts = [d.get("text", "")[:100] for d in dialogues[:3]]
    description = " ".join(description_parts) + "..."

    show_notes = f"""
## Episode: {topic}

### Highlights
{chr(10).join(['- ' + d.get('text', '')[:80] for d in dialogues[:5]])}

### Timestamps
- 00:00 - Introduction
- 02:00 - Main Discussion
- 08:00 - Key Insights
- 10:00 - Conclusion
    """

    return {
        "title": title,
        "description": description,
        "show_notes": show_notes,
        "tags": topic.lower().split()[:5],
    }


def publish_episode(episode_id: str, audio_url: str, metadata: Dict) -> str:
    """Publish episode and generate RSS feed"""

    supabase = get_supabase()

    result = supabase.table("episodes").select("channel_id").eq("id", episode_id).execute()
    if result.data:
        channel_id = result.data[0]["channel_id"]
        channel_result = supabase.table("channels").select("name").eq("id", channel_id).execute()
        channel_name = channel_result.data[0]["name"] if channel_result.data else "PodFlow"
    else:
        channel_name = "PodFlow"
        channel_id = None

    if channel_id:
        episodes_result = supabase.table("episodes").select("*").eq("channel_id", channel_id).order("created_at", desc=True).execute()
    else:
        episodes_result = supabase.table("episodes").select("*").order("created_at", desc=True).limit(10).execute()

    episodes_for_rss = []
    for ep in episodes_result.data:
        ep_metadata = ep.get("metadata") or {}
        if not isinstance(ep_metadata, dict):
            ep_metadata = {}
        episodes_for_rss.append({
            "title": ep_metadata.get("title", ep.get("topic", "Untitled")),
            "description": ep_metadata.get("description", ""),
            "audio_url": ep.get("audio_url", ""),
            "audio_length": 0,
            "published_at": ep.get("created_at", ""),
            "duration": "00:00",
        })

    rss_feed = generate_rss_feed(channel_name, episodes_for_rss)

    import os
    rss_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rss_files")
    os.makedirs(rss_dir, exist_ok=True)
    rss_path = os.path.join(rss_dir, f"{channel_id or 'default'}.xml")
    with open(rss_path, "w", encoding="utf-8") as f:
        f.write(rss_feed)

    return rss_path
