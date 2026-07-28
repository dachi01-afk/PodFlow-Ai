from celery_app import celery_app
from app.core.supabase_client import get_supabase
from app.agents.research import research_topic
from app.agents.scriptwriter import generate_script
from app.agents.audio import generate_episode_audio
from app.agents.distribution import generate_metadata, publish_episode
from app.utils.audio import generate_waveform_video
import os
from datetime import datetime, timezone

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_files")
VIDEO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "video_files")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def _fail_episode(episode_id: str, error: str):
    """Mark episode as failed with error message"""
    supabase = get_supabase()
    supabase.table("episodes").update({
        "status": "failed",
        "error": error,
    }).eq("id", episode_id).execute()


@celery_app.task(bind=True, name="app.tasks.pipeline.run_research_agent")
def run_research_agent(self, episode_id: str):
    """Agent 1: Research - Riset topik menggunakan Qwen API"""
    supabase = get_supabase()

    try:
        result = supabase.table("episodes").select("topic").eq("id", episode_id).execute()
        if not result.data:
            raise Exception(f"Episode {episode_id} not found")

        topic = result.data[0]["topic"]

        supabase.table("episodes").update({"status": "researching"}).eq(
            "id", episode_id
        ).execute()

        research_result = research_topic(topic)

        supabase.table("episodes").update(
            {"metadata": {"research": research_result}, "status": "writing"}
        ).eq("id", episode_id).execute()

        celery_app.send_task(
            "app.tasks.pipeline.run_scriptwriter_agent",
            args=[episode_id, research_result],
        )
        return {"episode_id": episode_id, "status": "research_done", "research": research_result}
    except Exception as e:
        _fail_episode(episode_id, str(e))
        raise


@celery_app.task(bind=True, name="app.tasks.pipeline.run_scriptwriter_agent")
def run_scriptwriter_agent(self, episode_id: str, research: dict):
    """Agent 2: Scriptwriter - Menulis dialog podcast menggunakan Agnes AI"""
    supabase = get_supabase()

    try:
        result = supabase.table("episodes").select("topic").eq("id", episode_id).execute()
        if not result.data:
            raise Exception(f"Episode {episode_id} not found")

        topic = result.data[0]["topic"]

        supabase.table("episodes").update({"status": "writing"}).eq(
            "id", episode_id
        ).execute()

        script_result = generate_script(topic, research)

        supabase.table("episodes").update(
            {"script": {"dialogues": script_result}, "status": "producing"}
        ).eq("id", episode_id).execute()

        celery_app.send_task(
            "app.tasks.pipeline.run_audio_agent",
            args=[episode_id, {"dialogues": script_result}],
        )
        return {"episode_id": episode_id, "status": "script_done", "script": {"dialogues": script_result}}
    except Exception as e:
        _fail_episode(episode_id, str(e))
        raise


@celery_app.task(bind=True, name="app.tasks.pipeline.run_audio_agent")
def run_audio_agent(self, episode_id: str, script: dict):
    """Agent 3: Audio - Generate audio + waveform video dari script"""
    supabase = get_supabase()

    try:
        supabase.table("episodes").update({"status": "producing"}).eq(
            "id", episode_id
        ).execute()

        dialogues = script.get("dialogues", [])
        audio_path = generate_episode_audio(dialogues)

        final_audio_path = os.path.join(AUDIO_DIR, f"{episode_id}.mp3")
        os.rename(audio_path, final_audio_path)

        video_path = os.path.join(VIDEO_DIR, f"{episode_id}.mp4")
        generate_waveform_video(final_audio_path, video_path)

        audio_url = f"/audio/{episode_id}.mp3"
        video_url = f"/video/{episode_id}.mp4"

        supabase.table("episodes").update({
            "audio_url": audio_url,
            "metadata": {"video_url": video_url},
            "status": "publishing",
        }).eq("id", episode_id).execute()

        celery_app.send_task(
            "app.tasks.pipeline.run_distribution_agent",
            args=[episode_id, {"audio_url": audio_url, "video_url": video_url}],
        )
        return {"episode_id": episode_id, "status": "audio_done", "audio_url": audio_url, "video_url": video_url}
    except Exception as e:
        _fail_episode(episode_id, str(e))
        raise


@celery_app.task(bind=True, name="app.tasks.pipeline.run_distribution_agent")
def run_distribution_agent(self, episode_id: str, audio: dict):
    """Agent 4: Distribution - Generate metadata dan RSS feed"""
    supabase = get_supabase()

    try:
        supabase.table("episodes").update({"status": "publishing"}).eq(
            "id", episode_id
        ).execute()

        result = supabase.table("episodes").select("topic, script, metadata").eq("id", episode_id).execute()
        if not result.data:
            raise Exception(f"Episode {episode_id} not found")

        episode = result.data[0]
        topic = episode["topic"]
        script = episode.get("script", {})
        old_metadata = episode.get("metadata") or {}

        metadata = generate_metadata(topic, script)

        if "video_url" in old_metadata:
            metadata["video_url"] = old_metadata["video_url"]

        audio_url = audio.get("audio_url", "")
        rss_path = publish_episode(episode_id, audio_url, metadata)

        supabase.table("episodes").update({
            "metadata": metadata,
            "status": "completed",
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", episode_id).execute()

        return {"episode_id": episode_id, "status": "completed", "metadata": metadata, "rss_path": rss_path}
    except Exception as e:
        _fail_episode(episode_id, str(e))
        raise
