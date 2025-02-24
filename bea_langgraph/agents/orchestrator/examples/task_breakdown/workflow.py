"""
Complex task breakdown example using orchestrator-workers pattern.

This example demonstrates breaking down a complex task into manageable subtasks
and processing them using worker agents.
"""

from typing import List, Dict, Any
from ...models import Task, SubTask, OrchestratorConfig
from ...workflow import OrchestratorWorkflow
from ....basic_workflow.api.client import VeniceClient

class TaskBreakdownWorkflow(OrchestratorWorkflow):
    """Implementation of complex task breakdown workflow."""
    
    async def process_complex_task(self, task_description: str) -> str:
        """Process a complex task by breaking it down."""
        # Create task
        task = Task(description=task_description)
        
        # Execute task with breakdown and synthesis
        result = await self.execute(task)
        return result.result
        
    async def _break_down_task(self, task: Task) -> List[SubTask]:
        """Specialized task breakdown for complex tasks."""
        messages = [
            {"role": "system", "content": """Break down this complex task into smaller, manageable subtasks.
            Each subtask should be self-contained and independently processable."""},
            {"role": "user", "content": f"Complex task to break down:\n{task.description}"}
        ]
        
        result_buffer = []
        async for chunk in self.client.stream_completion(messages):
            if chunk.startswith("<think>"):
                print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                continue
            result_buffer.append(chunk)
            
        # Parse subtasks from result
        subtasks_text = "".join(result_buffer).split("\n")
        return [
            SubTask(
                task_id=f"subtask_{i}",
                description=text.strip()
            )
            for i, text in enumerate(subtasks_text)
            if text.strip()
        ][:self.config.max_subtasks]
