import subprocess
import os
from pydub import AudioSegment


def text_to_speech(text: str, output_path: str, lang: str = 'id') -> str:
    """Convert text to speech using gTTS."""
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path


def create_silence(duration_ms: int) -> AudioSegment:
    """Create silence audio segment."""
    return AudioSegment.silent(duration=duration_ms)


def merge_audio_segments(segments: list[str], output_path: str) -> str:
    """Merge multiple audio segments into one file."""
    combined = AudioSegment.empty()
    
    for segment_path in segments:
        audio = AudioSegment.from_file(segment_path)
        combined += audio
    
    combined.export(output_path, format="mp3", bitrate="192k")
    return output_path


def cleanup_temp_files(file_paths: list[str]):
    """Remove temporary audio files."""
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)
