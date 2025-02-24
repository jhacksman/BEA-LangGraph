"""
Result synthesis example using orchestrator-workers pattern.

This example demonstrates synthesizing results from multiple subtasks into
a coherent final output.
"""

from typing import List, Dict, Any
from ...models import Task, SubTask, OrchestratorConfig
from ...workflow import OrchestratorWorkflow
from ....basic_workflow.api.client import VeniceClient

class SynthesisWorkflow(OrchestratorWorkflow):
    """Implementation of result synthesis workflow."""
    
    async def synthesize_results(self, results: List[str], context: str) -> str:
        """Synthesize multiple results with context."""
        # Create task with synthesis context
        task = Task(
            description=f"Synthesize these results in the context of: {context}",
            subtasks=[
                SubTask(
                    task_id=f"result_{i}",
                    description=result,
                    result=result
                )
                for i, result in enumerate(results)
            ]
        )
        
        # Execute task focusing on synthesis
        result = await self.execute(task)
        return result.result
        
    async def _synthesize_results(self, subtasks: List[SubTask]) -> str:
        """Specialized synthesis for combining multiple results."""
        # Prepare results for synthesis
        results_text = "\n".join(
            f"Result {subtask.task_id}:\n{subtask.result}"
            for subtask in subtasks
            if subtask.result and not subtask.result.startswith("Error:")
        )
        
        messages = [
            {"role": "system", "content": """Synthesize these results into a coherent output.
            Focus on combining key insights and maintaining consistency."""},
            {"role": "user", "content": f"Results to synthesize:\n{results_text}"}
        ]
        
        result_buffer = []
        async for chunk in self.client.stream_completion(messages):
            if chunk.startswith("<think>"):
                print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                continue
            result_buffer.append(chunk)
            
        return "".join(result_buffer)
