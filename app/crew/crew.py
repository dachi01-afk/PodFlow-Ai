from typing import List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
from .agents import Agent
from .tasks import Task


class Process(Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"


@dataclass
class Crew:
    agents: List[Agent]
    tasks: List[Task]
    process: Process = Process.sequential
    verbose: bool = False
    step_callback: Optional[Callable[[int, Agent, dict], None]] = None

    def kickoff(self, inputs: dict = None) -> dict:
        context = inputs or {}
        final_output = {}

        for i, task in enumerate(self.tasks):
            agent = self.agents[i]
            task.agent = agent

            if self.verbose:
                print(f"\n{'='*60}")
                print(f"Agent {i+1}: {agent.role}")
                print(f"Task: {task.description[:80]}...")
                print(f"{'='*60}")

            context["task_description"] = task.description
            output = agent.execute(task.description, context)
            final_output[agent.role] = output
            context[f"agent_{i+1}_output"] = output

            if self.step_callback:
                self.step_callback(i, agent, output)

        return final_output
