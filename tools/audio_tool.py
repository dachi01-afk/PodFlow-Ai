import json
from crewai.tools import BaseTool
from agents.audio_agent import AudioAgent


class AudioTool(BaseTool):
    name: str = "Generate Podcast Audio"
    description: str = "Convert podcast script dialogue to audio file. Input should be JSON string with dialogue array containing text and pause_duration fields."
    
    def _run(self, script_data: str) -> str:
        try:
            if isinstance(script_data, str):
                script_dict = json.loads(script_data)
            else:
                script_dict = script_data
            
            agent = AudioAgent()
            audio_path = agent.produce_audio(script_dict)
            return f"Audio generated successfully: {audio_path}"
        except Exception as e:
            return f"Error generating audio: {str(e)}"
