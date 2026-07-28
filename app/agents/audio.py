import httpx
import tempfile
import os
from typing import List, Dict
from config import get_settings
from app.utils.audio import concatenate_audio_files, generate_silence, generate_waveform_video

settings = get_settings()

VOICE_IDS = {
    "Host_A": "EXAVITQu4vr4xnSDxMaL",  # Sarah - Mature, Confident
    "Host_B": "JBFqnCBsd6RMkjVDRZzb",  # George - Warm, Storyteller
}


def text_to_speech(text: str, voice_id: str) -> bytes:
    """Convert text to speech using ElevenLabs API"""

    response = httpx.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": settings.elevenlabs_api_key,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
        },
        timeout=60.0,
    )

    response.raise_for_status()
    return response.content


def generate_episode_audio(dialogues: List[Dict]) -> str:
    """Generate audio for entire episode from dialogues"""

    audio_files = []

    for dialogue in dialogues:
        speaker = dialogue.get("speaker", "Host_A")
        text = dialogue.get("text", "")
        pause_duration = dialogue.get("pause_duration", 0.5)

        voice_id = VOICE_IDS.get(speaker, VOICE_IDS["Host_A"])

        audio_data = text_to_speech(text, voice_id)

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(audio_data)
            audio_files.append(f.name)

        if pause_duration > 0:
            pause_file = tempfile.mktemp(suffix='.mp3')
            generate_silence(pause_duration, pause_file)
            audio_files.append(pause_file)

    output_path = tempfile.mktemp(suffix='.mp3')
    concatenate_audio_files(audio_files, output_path)

    for f in audio_files:
        if os.path.exists(f):
            os.unlink(f)

    return output_path
