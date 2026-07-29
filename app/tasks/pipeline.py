from celery_app import celery_app
from app.core.supabase_client import get_supabase
from app.agents.audio import generate_episode_audio
from app.utils.audio import generate_waveform_video
from app.crew.tools import ResearchTool, ScriptTool, MetadataTool, PublishTool
import os
from datetime import datetime, timezone

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_files")
VIDEO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "video_files")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def _fail_episode(episode_id: str, error: str):
    supabase = get_supabase()
    supabase.table("episodes").update({
        "status": "failed",
        "error": error,
    }).eq("id", episode_id).execute()


def _update_status(episode_id: str, status: str, extra: dict = None):
    supabase = get_supabase()
    data = {"status": status}
    if extra:
        data.update(extra)
    supabase.table("episodes").update(data).eq("id", episode_id).execute()


@celery_app.task(bind=True, name="app.tasks.pipeline.run_pipeline")
def run_pipeline(self, episode_id: str):
    """Run full PodFlow pipeline using CrewAI-style orchestration (sequential agents)"""
    supabase = get_supabase()

    try:
        episode = supabase.table("episodes").select("*").eq("id", episode_id).execute()
        if not episode.data:
            raise Exception(f"Episode {episode_id} not found")

        episode = episode.data[0]
        topic = episode["topic"]

        # === Agent 1: Research (Qwen) ===
        _update_status(episode_id, "researching")
        research_result = ResearchTool().run(topic=topic)
        _update_status(episode_id, "writing", {"metadata": {"research": research_result}})

        # === Agent 2: Scriptwriter (Agnes AI) ===
        _update_status(episode_id, "writing")
        script_result = ScriptTool().run(topic=topic, research=research_result)
        _update_status(episode_id, "producing", {"script": {"dialogues": script_result}})

        # === Agent 3: Audio (ElevenLabs + FFmpeg) ===
        _update_status(episode_id, "producing")
        audio_path = generate_episode_audio(script_result)

        final_audio_path = os.path.join(AUDIO_DIR, f"{episode_id}.mp3")
        os.rename(audio_path, final_audio_path)

        video_path = os.path.join(VIDEO_DIR, f"{episode_id}.mp4")
        generate_waveform_video(final_audio_path, video_path)

        audio_url = f"/audio/{episode_id}.mp3"
        video_url = f"/video/{episode_id}.mp4"

        _update_status(episode_id, "publishing", {
            "audio_url": audio_url,
            "metadata": {"video_url": video_url},
        })

        # === Agent 4: Distribution (Metadata + RSS) ===
        _update_status(episode_id, "publishing")
        episode = supabase.table("episodes").select("topic, script, metadata").eq("id", episode_id).execute()
        episode = episode.data[0]
        old_metadata = episode.get("metadata") or {}

        metadata = MetadataTool().run(topic=topic, script={"dialogues": script_result})
        if "video_url" in old_metadata:
            metadata["video_url"] = old_metadata["video_url"]

        rss_path = PublishTool().run(episode_id=episode_id, audio_url=audio_url, metadata=metadata)

        _update_status(episode_id, "completed", {
            "metadata": metadata,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })

        return {
            "episode_id": episode_id,
            "status": "completed",
            "research": research_result,
            "script": script_result,
            "audio_url": audio_url,
            "video_url": video_url,
            "rss_path": rss_path,
        }

    except Exception as e:
        _fail_episode(episode_id, str(e))
        raise
