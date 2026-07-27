import json
from crewai.tools import BaseTool
from agents.metadata_agent import MetadataAgent


class MetadataTool(BaseTool):
    name: str = "Generate SEO Metadata"
    description: str = "Generate SEO metadata and social content. Input should be JSON string with script and research data."
    
    def _run(self, script_data: str, research_data: str) -> str:
        try:
            if isinstance(script_data, str):
                script_dict = json.loads(script_data)
            else:
                script_dict = script_data
            
            if isinstance(research_data, str):
                research_dict = json.loads(research_data)
            else:
                research_dict = research_data
            
            agent = MetadataAgent()
            metadata = agent.generate_metadata(script_dict, research_dict)
            social = agent.generate_social_content(script_dict, metadata)
            
            return json.dumps({
                "metadata_path": metadata.get("_file_path", ""),
                "social_path": social.get("_file_path", ""),
                "status": "success"
            })
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
