from openai import OpenAI
from pydantic import BaseModel
from config import AGNES_API_KEY, AGNES_BASE_URL, AGNES_MODEL
from utils.json_utils import validate_json_output


class DialogueLine(BaseModel):
    speaker: str
    emotion: str
    pause_duration: float
    text: str


class ScriptOutput(BaseModel):
    title: str
    description: str
    duration_estimate: str
    dialogue: list[DialogueLine]


SCRIPT_SYSTEM_PROMPT = """You are a creative podcast scriptwriter for Indonesian audience.

PERSONALITY:
- Host A: Formal expert, uses proper Bahasa Indonesia
- Host B: Casual skeptic, uses informal language + slang

STYLE:
- Conversational, like friends chatting
- Include humor and local references
- Use Indonesian slang naturally (gak, dong, sih, kok, etc.)
- Add emotional expressions (aduh, waduh, eh, eh tapi)

OUTPUT FORMAT (JSON):
{
  "title": "string",
  "description": "string",
  "duration_estimate": "1-2 minutes",
  "dialogue": [
    {
      "speaker": "Host_A|Host_B",
      "emotion": "emotion tag",
      "pause_duration": seconds,
      "text": "dialogue text"
    }
  ]
}

RULES:
1. Each dialogue line MUST have emotion tag
2. Add pause_duration for dramatic effect (1-3 seconds)
3. Keep total duration 1-2 minutes (approximately 200-300 words)
4. Start with engaging hook (first 30 seconds)
5. End with memorable conclusion"""


class ScriptAgent:
    def __init__(self):
        self.client = OpenAI(api_key=AGNES_API_KEY, base_url=AGNES_BASE_URL)
    
    def write_script(self, research_data: dict) -> ScriptOutput:
        """Write a podcast script based on research data."""
        user_prompt = f"""Based on this research, write a podcast script:

Topic: {research_data.get('topic', 'Unknown')}
Key Facts: {', '.join(research_data.get('key_facts', []))}
Sentiment: {research_data.get('sentiment', 'neutral')}
Trending Angles: {', '.join(research_data.get('trending_angles', []))}"""
        
        response = self.client.chat.completions.create(
            model=AGNES_MODEL,
            messages=[
                {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        raw_output = response.choices[0].message.content
        if not raw_output:
            raise ValueError("Script Agent received empty response from LLM")
        json_data = validate_json_output(raw_output)
        
        return ScriptOutput(**json_data)
