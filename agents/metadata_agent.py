import json
import os
from datetime import datetime
from config import METADATA_DIR, SOCIAL_DIR


class MetadataAgent:
    def __init__(self):
        os.makedirs(METADATA_DIR, exist_ok=True)
        os.makedirs(SOCIAL_DIR, exist_ok=True)
    
    def generate_metadata(self, script_data: dict, research_data: dict) -> dict:
        """Generate SEO-optimized metadata and social content."""
        title = script_data.get('title', 'Podcast Episode')
        description = script_data.get('description', '')
        topic = research_data.get('topic', '')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        metadata = {
            "title": f"{title} | PodFlow AI",
            "description": f"{description}\n\nTopik: {topic}\n\nDiproduksi oleh PodFlow AI - Autonomous Podcast Network",
            "tags": [topic.lower(), "podcast", "indonesia", "ai"],
            "duration": script_data.get('duration_estimate', '1-2 minutes'),
            "created_at": datetime.now().isoformat()
        }
        
        metadata_path = os.path.join(METADATA_DIR, f"metadata_{timestamp}.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        metadata["_file_path"] = metadata_path
        return metadata
    
    def generate_social_content(self, script_data: dict, metadata: dict) -> dict:
        """Generate social media content for repurposing."""
        title = metadata.get('title', '')
        description = metadata.get('description', '')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        social = {
            "show_notes": f"## {title}\n\n{description}",
            "x_thread": [
                f"Pod baru aja rilis: {title}\n\nThread ini jelasin apa yang dibahas 👇",
                f"1/ {description[:200]}...",
                f"2/ Dengarkan sekarang di PodFlow AI!",
                f"#Podcast #AI #Indonesia"
            ],
            "linkedin_post": f"New Episode: {title}\n\n{description}\n\n#Podcast #AI #Indonesia #ContentCreation"
        }
        
        social_path = os.path.join(SOCIAL_DIR, f"social_content_{timestamp}.json")
        with open(social_path, 'w', encoding='utf-8') as f:
            json.dump(social, f, ensure_ascii=False, indent=2)
        
        social["_file_path"] = social_path
        return social
