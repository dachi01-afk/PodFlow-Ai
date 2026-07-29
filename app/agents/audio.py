import httpx
import json
import subprocess
import tempfile
import os
from typing import List, Dict

from config import get_settings
from app.utils.audio import (
    concatenate_audio_files,
    generate_silence,
    generate_waveform_video,
)

settings = get_settings()

VOICE_IDS = {
    "Host_A": "EXAVITQu4vr4xnSDxMaL",
    "Host_B": "JBFqnCBsd6RMkjVDRZzb",
}


def text_to_speech(text: str, voice_id: str) -> bytes:
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


def get_audio_duration(audio_path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            audio_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def generate_episode_audio(dialogues: List[Dict]):
    """
    Returns:
    {
        "audio_path": "...",
        "segments": [...]
    }
    """

    audio_files = []
    segments = []
    current_time = 0.0

    for dialogue in dialogues:
        speaker = dialogue.get("speaker", "Host_A")
        text = dialogue.get("text", "")
        pause_duration = dialogue.get("pause_duration", 0.5)

        voice_id = VOICE_IDS.get(speaker, VOICE_IDS["Host_A"])

        audio_data = text_to_speech(text, voice_id)

        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False,
        ) as f:
            f.write(audio_data)
            temp_audio = f.name

        audio_files.append(temp_audio)

        duration = get_audio_duration(temp_audio)

        segments.append(
            {
                "speaker": speaker,
                "text": text,
                "start": current_time,
                "end": current_time + duration,
            }
        )

        current_time += duration

        if pause_duration > 0:
            pause_file = tempfile.mktemp(suffix=".mp3")
            generate_silence(pause_duration, pause_file)

            audio_files.append(pause_file)
            current_time += pause_duration

    output_path = tempfile.mktemp(suffix=".mp3")
    concatenate_audio_files(audio_files, output_path)

    for file in audio_files:
        if os.path.exists(file):
            os.unlink(file)

    import json

    with open("app/audio_files/test_segments.json", "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=4, ensure_ascii=False)

    return {
        "audio_path": output_path,
        "segments": segments,
    }