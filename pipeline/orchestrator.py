import json
from typing import Callable, Optional
from agents import ResearchAgent, ScriptAgent, AudioAgent, MetadataAgent


class PipelineOrchestrator:
    def __init__(self, status_callback: Optional[Callable] = None):
        self.research_agent = ResearchAgent()
        self.script_agent = ScriptAgent()
        self.audio_agent = AudioAgent()
        self.metadata_agent = MetadataAgent()
        self.status_callback = status_callback
    
    def _update_status(self, agent_name: str, status: str, progress: int):
        if self.status_callback:
            self.status_callback(agent_name, status, progress)
    
    def run(self, topic: str) -> dict:
        """Execute the full pipeline."""
        results = {}
        
        try:
            self._update_status("Research Agent", "running", 0)
            research = self.research_agent.research(topic)
            results['research'] = research.model_dump()
            self._update_status("Research Agent", "completed", 100)
            
            self._update_status("Script Writer", "running", 0)
            script = self.script_agent.write_script(results['research'])
            results['script'] = script.model_dump()
            self._update_status("Script Writer", "completed", 100)
            
            self._update_status("Audio Engine", "running", 0)
            audio_path = self.audio_agent.produce_audio(results['script'])
            results['audio_path'] = audio_path
            self._update_status("Audio Engine", "completed", 100)
            
            self._update_status("Metadata Engine", "running", 0)
            metadata = self.metadata_agent.generate_metadata(
                results['script'], 
                results['research']
            )
            social = self.metadata_agent.generate_social_content(
                results['script'], 
                metadata
            )
            results['metadata'] = metadata
            results['social'] = social
            self._update_status("Metadata Engine", "completed", 100)
            
            return results
        
        except Exception as e:
            self._update_status("Error", str(e), 0)
            raise
