from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time


class CLIDashboard:
    def __init__(self):
        self.console = Console()
        self.agents = {
            "Research Agent": {"status": "pending", "progress": 0},
            "Script Writer": {"status": "pending", "progress": 0},
            "Audio Engine": {"status": "pending", "progress": 0},
            "Metadata Engine": {"status": "pending", "progress": 0}
        }
        self.start_time = None
    
    def start(self, topic: str):
        self.start_time = time.time()
        self.console.clear()
        self.console.print(Panel.fit(
            "[bold cyan]PODFLOW AI - Autonomous Podcast Network[/bold cyan]",
            subtitle="Pipeline Status"
        ))
        self.console.print(f"\n[bold]Topic:[/bold] {topic}\n")
    
    def update_status(self, agent_name: str, status: str, progress: int):
        if agent_name in self.agents:
            self.agents[agent_name]["status"] = status
            self.agents[agent_name]["progress"] = progress
            self._render()
        elif agent_name == "Error":
            self.console.print(f"\n[bold red]ERROR:[/bold red] {status}")
    
    def _render(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Progress")
        
        for name, info in self.agents.items():
            status = info["status"]
            progress = info["progress"]
            
            if status == "completed":
                status_display = "[green]✓ COMPLETED[/green]"
                bar = "█" * 20
            elif status == "running":
                status_display = "[yellow]⟳ RUNNING[/yellow]"
                filled = int(progress / 5)
                bar = "█" * filled + "░" * (20 - filled)
            else:
                status_display = "[dim]○ PENDING[/dim]"
                bar = "░" * 20
            
            table.add_row(name, status_display, bar)
        
        self.console.print(table)
    
    def finish(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.console.print(f"\n[bold green]Pipeline completed in {elapsed:.1f}s[/bold green]")
