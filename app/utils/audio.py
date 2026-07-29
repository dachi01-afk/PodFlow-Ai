import subprocess
import tempfile
import os
from typing import List
from app.utils.video import VideoComposer


def concatenate_audio_files(audio_files: List[str], output_path: str) -> str:
    """Concatenate multiple audio files using FFmpeg"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")
        file_list = f.name

    try:
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", file_list,
            "-c", "copy",
            output_path,
            "-y"
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    finally:
        os.unlink(file_list)


def apply_audio_ducking(vocal_path: str, bgm_path: str, output_path: str) -> str:
    """Apply audio ducking - lower BGM volume when vocal is active"""

    cmd = [
        "ffmpeg",
        "-i", vocal_path,
        "-i", bgm_path,
        "-filter_complex",
        "[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2:duration=first",
        output_path,
        "-y"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def generate_silence(duration: float, output_path: str) -> str:
    """Generate silence audio file"""

    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=mono",
        "-t", str(duration),
        output_path,
        "-y"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

def generate_waveform_video(
    audio_path: str,
    output_path: str,
    title: str = "AI Generated Podcast",
    segments=None,
) -> str:
    
    composer = VideoComposer()

    return composer.compose(
        audio_path=audio_path,
        output_path=output_path,
        title=title,
        segments=segments,
    )