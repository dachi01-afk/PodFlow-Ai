from dataclasses import dataclass
from typing import Optional
from .agents import Agent


@dataclass
class Task:
    description: str
    agent: Agent
    expected_output: str
    context: Optional[dict] = None


research_task = Task(
    description="Lakukan riset mendalam tentang topik podcast yang diberikan",
    agent=None,
    expected_output="""JSON dengan struktur:
    {
        "summary": "ringkasan topik",
        "key_facts": ["fakta1", "fakta2", ...],
        "trends": ["tren1", "tren2", ...],
        "sentiment": "positif/negatif/netral",
        "sources": ["sumber1", "sumber2", ...]
    }""",
)

script_task = Task(
    description="""Tulis dialog podcast antara 2 host berdasarkan hasil riset.
    Host A: Pakar formal yang memberi penjelasan
    Host B: Pemula kritis yang bertanya""",
    agent=None,
    expected_output="""JSON array dengan struktur:
    [
        {
            "speaker": "Host_A/Host_B",
            "emotion": "enthusiastic/confused/neutral/thinking/excited",
            "pause_duration": 0.5-2.0,
            "text": "dialog text"
        }
    ]""",
)

audio_task = Task(
    description="Produksi file audio dari dialog yang telah ditulis",
    agent=None,
    expected_output="Path ke file audio MP3 yang sudah jadi",
)

distribution_task = Task(
    description="Generate metadata SEO dan publish episode ke RSS feed",
    agent=None,
    expected_output="URL RSS feed dan metadata episode",
)
