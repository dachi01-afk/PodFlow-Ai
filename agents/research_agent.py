from groq import Groq
from pydantic import BaseModel
from config import GROQ_API_KEY, GROQ_BASE_URL, QWEN_MODEL
from utils.json_utils import validate_json_output


class ResearchOutput(BaseModel):
    topic: str
    key_facts: list[str]
    sentiment: str
    trending_angles: list[str]
    sources: list[str]


RESEARCH_SYSTEM_PROMPT = """You are an expert research analyst specializing in Indonesian market trends.

TASK: Research the given topic and extract key insights.

OUTPUT FORMAT (JSON):
{
  "topic": "string",
  "key_facts": ["array of key facts"],
  "sentiment": "positive|negative|neutral",
  "trending_angles": ["array of trending angles"],
  "sources": ["array of source references"]
}

RULES:
1. Focus on facts, not opinions
2. Include local Indonesian context
3. Filter out hoaxes and misinformation
4. Prioritize recent data (last 7 days)
5. Output MUST be valid JSON"""


class ResearchAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)
    
    def research(self, topic: str) -> ResearchOutput:
        """Research a topic and return structured insights."""
        response = self.client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": RESEARCH_SYSTEM_PROMPT},
                {"role": "user", "content": f"Research this topic: {topic}"}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        raw_output = response.choices[0].message.content
        if not raw_output:
            raise ValueError("Research Agent received empty response from LLM")
        json_data = validate_json_output(raw_output)
        
        return ResearchOutput(**json_data)
