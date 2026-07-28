import subprocess
import tempfile
import os
from typing import List


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


def generate_waveform_video(audio_path: str, output_path: str) -> str:
    """Generate 9:16 waveform video from audio using FFmpeg showwaves"""

    video_only = output_path + ".tmp.mp4"

    try:
        cmd_video = [
            "ffmpeg",
            "-i", audio_path,
            "-filter_complex",
            "[0:a]showwaves=s=1080x1920:mode=cline:rate=24:colors=0x00D4FF[v]",
            "-map", "[v]",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "32",
            "-pix_fmt", "yuv420p",
            "-an",
            video_only,
            "-y"
        ]
        subprocess.run(cmd_video, check=True, capture_output=True)

        cmd_mux = [
            "ffmpeg",
            "-i", video_only,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path,
            "-y"
        ]
        subprocess.run(cmd_mux, check=True, capture_output=True)
    finally:
        if os.path.exists(video_only):
            os.unlink(video_only)

    return output_path
