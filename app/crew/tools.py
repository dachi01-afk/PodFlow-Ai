from app.agents.research import research_topic
from app.agents.scriptwriter import generate_script
from app.agents.audio import generate_episode_audio
from app.agents.distribution import generate_metadata, publish_episode


class ResearchTool:
    name: str = "Research Tool"
    description: str = "Meneliti topik tren terkini menggunakan Qwen API"

    def run(self, topic: str) -> dict:
        return research_topic(topic)


class ScriptTool:
    name: str = "Scriptwriting Tool"
    description: str = "Menulis dialog podcast natural menggunakan Agnes AI"

    def run(self, topic: str, research: dict) -> list:
        return generate_script(topic, research)


class AudioTool:
    name: str = "Audio Production Tool"
    description: str = "Memproduksi audio podcast via ElevenLabs + FFmpeg"

    def run(self, dialogues: list) -> str:
        return generate_episode_audio(dialogues)


class MetadataTool:
    name: str = "Metadata Generation Tool"
    description: str = "Menghasilkan metadata SEO dan show notes"

    def run(self, topic: str, script: dict) -> dict:
        return generate_metadata(topic, script)


class PublishTool:
    name: str = "Publishing Tool"
    description: str = "Mempublikasikan episode dan menghasilkan RSS feed"

    def run(self, episode_id: str, audio_url: str, metadata: dict) -> str:
        return publish_episode(episode_id, audio_url, metadata)
