import os
import tempfile
from pydub import AudioSegment
from config import AUDIO_DIR
from utils.audio_utils import text_to_speech, merge_audio_segments, create_silence


class AudioAgent:
    def __init__(self):
        os.makedirs(AUDIO_DIR, exist_ok=True)
    
    def produce_audio(self, script_data: dict, filename: str = "podcast") -> str:
        """Convert script to audio file."""
        dialogue = script_data.get('dialogue', [])
        if not dialogue:
            raise ValueError("No dialogue lines found in script")
        
        temp_files = []
        total = len(dialogue)
        
        try:
            for i, line in enumerate(dialogue):
                text = line.get('text', '')
                pause_duration = line.get('pause_duration', 1.0)
                
                speech_path = os.path.join(tempfile.gettempdir(), f"speech_{i}.mp3")
                text_to_speech(text, speech_path)
                temp_files.append(speech_path)
                
                if i < total - 1:
                    pause_ms = int(pause_duration * 1000)
                    silence_path = os.path.join(tempfile.gettempdir(), f"silence_{i}.mp3")
                    silence = create_silence(pause_ms)
                    silence.export(silence_path, format="mp3")
                    temp_files.append(silence_path)
            
            output_path = os.path.join(AUDIO_DIR, f"{filename}.mp3")
            merge_audio_segments(temp_files, output_path)
            
            return output_path
        
        finally:
            for f in temp_files:
                if os.path.exists(f):
                    os.remove(f)
