import yaml
from crewai import Agent, Task, Crew, Process
from config import GROQ_API_KEY, AGNES_API_KEY
from tools import AudioTool, MetadataTool


def load_yaml(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def create_crew(topic: str) -> Crew:
    agents_config = load_yaml('config/agents.yaml')
    tasks_config = load_yaml('config/tasks.yaml')
    
    # LLM configurations
    qwen_llm = {
        "model": "qwen/qwen3.6-27b",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": GROQ_API_KEY
    }
    
    agnes_llm = {
        "model": "agnes-2.0-flash",
        "base_url": "https://apihub.agnes-ai.com/v1",
        "api_key": AGNES_API_KEY
    }
    
    # Create agents
    researcher = Agent(
        config=agents_config['researcher'],
        llm=qwen_llm,
        verbose=True
    )
    
    script_writer = Agent(
        config=agents_config['script_writer'],
        llm=agnes_llm,
        verbose=True
    )
    
    audio_producer = Agent(
        config=agents_config['audio_producer'],
        tools=[AudioTool()],
        verbose=True
    )
    
    seo_specialist = Agent(
        config=agents_config['seo_specialist'],
        tools=[MetadataTool()],
        verbose=True
    )
    
    # Create tasks
    research_task = Task(
        config=tasks_config['research_task'],
        agent=researcher
    )
    
    script_task = Task(
        config=tasks_config['script_task'],
        agent=script_writer,
        context=[research_task]
    )
    
    audio_task = Task(
        config=tasks_config['audio_task'],
        agent=audio_producer,
        context=[script_task]
    )
    
    metadata_task = Task(
        config=tasks_config['metadata_task'],
        agent=seo_specialist,
        context=[script_task, research_task]
    )
    
    # Create crew
    crew = Crew(
        agents=[researcher, script_writer, audio_producer, seo_specialist],
        tasks=[research_task, script_task, audio_task, metadata_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew
