from typing import Optional
from dataclasses import dataclass, field
from .tools import ResearchTool, ScriptTool, AudioTool, MetadataTool


@dataclass
class Agent:
    role: str
    goal: str
    backstory: str
    tools: list = field(default_factory=list)
    llm: Optional[str] = None
    allow_delegation: bool = False
    verbose: bool = False

    def execute(self, task_description: str, context: Optional[dict] = None) -> dict:
        result = {}
        for tool in self.tools:
            if context:
                result = tool.run(**context)
            else:
                result = tool.run(task_description)
        return result if result else {"output": f"{self.role} executed: {task_description}"}


research_agent = Agent(
    role="Research Specialist",
    goal="Meneliti topik tren terkini dengan fakta akurat dan sumber terpercaya",
    backstory="""Anda adalah peneliti ahli dengan pengalaman 10+ tahun di jurnalisme data.
    Anda mampu menyaring hoaks, mengekstrak sentimen publik, dan menyajikan riset
    dalam format terstruktur yang mudah dipahami.""",
    tools=[ResearchTool()],
    llm="Qwen (via Groq)",
    verbose=True,
)

scriptwriter_agent = Agent(
    role="Dialogue Scriptwriter",
    goal="Menulis dialog podcast yang natural, emosional, dan engaging antara 2 host",
    backstory="""Anda adalah penulis skenario podcast profesional yang menguasai
    seni dialog. Anda paham cara membangun ketegangan, melemparkan humor,
    dan menciptakan momen emosional yang membuat pendengar betah.""",
    tools=[ScriptTool()],
    llm="Agnes AI",
    verbose=True,
)

audio_agent = Agent(
    role="Audio Engineer",
    goal="Memproduksi audio podcast berkualitas studio dengan intonasi natural",
    backstory="""Anda adalah sound engineer yang berpengalaman dengan ElevenLabs
    dan FFmpeg. Anda memastikan setiap jeda emosional tepat, suara jernih,
    dan output siap distribusi.""",
    tools=[AudioTool()],
    verbose=True,
)

distribution_agent = Agent(
    role="Distribution Manager",
    goal="Mengoptimalkan metadata SEO dan mempublikasikan episode ke RSS feed",
    backstory="""Anda adalah spesialis SEO podcast yang memastikan setiap episode
    mudah ditemukan di Spotify, Apple Podcasts, dan platform streaming lainnya.
    Anda juga ahli dalam menghasilkan RSS feed yang valid.""",
    tools=[MetadataTool()],
    verbose=True,
)
