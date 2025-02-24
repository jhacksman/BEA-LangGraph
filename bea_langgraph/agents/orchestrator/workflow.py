"""
Orchestrator workflow implementation.

This module implements the orchestrator-workers pattern from Anthropic's research,
providing functionality for task breakdown, delegation, and result synthesis.
"""

import asyncio
from typing import List, Dict, Any, Optional
from .models import Task, SubTask, OrchestratorConfig
from ..basic_workflow.api.client import VeniceClient

class OrchestratorWorkflow:
    """Implementation of orchestrator-workers workflow."""
    
    def __init__(self, config: OrchestratorConfig, client: VeniceClient):
        """Initialize workflow with configuration and API client."""
        self.config = config
        self.client = client
        
    async def execute(self, task: Task) -> Task:
        """Execute a complex task using orchestrator-workers pattern."""
        try:
            # Break down task into subtasks
            subtasks = await self._break_down_task(task)
            task.subtasks = subtasks
            
            # Process subtasks with workers
            results = await self._delegate_tasks(subtasks)
            
            # Synthesize results
            final_result = await self._synthesize_results(results)
            task.result = final_result
            
            return task
            
        except Exception as e:
            print(f"Error in orchestrator workflow: {str(e)}")
            raise
            
    async def _break_down_task(self, task: Task) -> List[SubTask]:
        """Break down complex task into subtasks."""
        try:
            messages = [
                {"role": "system", "content": "Break down this task into smaller, manageable subtasks."},
                {"role": "user", "content": f"Task to break down: {task.description}"}
            ]
            
            result_buffer = []
            async with asyncio.timeout(self.config.timeout_per_subtask):
                async for chunk in self.client.stream_completion(messages):
                    if chunk.startswith("<think>"):
                        print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                        continue
                    result_buffer.append(chunk)
                    
            # Parse subtasks from result
            subtasks_text = "".join(result_buffer).split("\n")
            subtasks = [
                SubTask(
                    task_id=f"subtask_{i}",
                    description=text.strip()
                )
                for i, text in enumerate(subtasks_text)
                if text.strip()
            ][:self.config.max_subtasks]
            
            return subtasks
            
        except Exception as e:
            print(f"Error breaking down task: {str(e)}")
            raise
            
    async def _delegate_tasks(self, subtasks: List[SubTask]) -> List[SubTask]:
        """Delegate subtasks to workers."""
        try:
            # Process subtasks concurrently
            async with asyncio.timeout(self.config.timeout_per_subtask):
                results = await asyncio.gather(
                    *[self._process_subtask(subtask) for subtask in subtasks],
                    return_exceptions=True
                )
            
            # Handle results and exceptions
            processed_subtasks = []
            for subtask, result in zip(subtasks, results):
                if isinstance(result, Exception):
                    print(f"Error processing subtask {subtask.task_id}: {str(result)}")
                    subtask.result = f"Error: {str(result)}"
                else:
                    subtask.result = result
                processed_subtasks.append(subtask)
                
            return processed_subtasks
            
        except Exception as e:
            print(f"Error delegating tasks: {str(e)}")
            raise
            
    async def _process_subtask(self, subtask: SubTask) -> str:
        """Process a single subtask."""
        messages = [
            {"role": "system", "content": "Process this subtask efficiently and accurately."},
            {"role": "user", "content": subtask.description}
        ]
        
        result_buffer = []
        async for chunk in self.client.stream_completion(messages):
            if chunk.startswith("<think>"):
                print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                continue
            result_buffer.append(chunk)
            
        return "".join(result_buffer)
        
    async def _synthesize_results(self, subtasks: List[SubTask]) -> str:
        """Synthesize results from completed subtasks."""
        try:
            # Prepare results for synthesis
            results_text = "\n".join(
                f"Subtask {subtask.task_id}: {subtask.result}"
                for subtask in subtasks
                if subtask.result and not subtask.result.startswith("Error:")
            )
            
            messages = [
                {"role": "system", "content": "Synthesize these subtask results into a coherent final result."},
                {"role": "user", "content": f"Subtask results to synthesize:\n{results_text}"}
            ]
            
            result_buffer = []
            async with asyncio.timeout(self.config.synthesis_timeout):
                async for chunk in self.client.stream_completion(messages):
                    if chunk.startswith("<think>"):
                        print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                        continue
                    result_buffer.append(chunk)
                    
            return "".join(result_buffer)
            
        except Exception as e:
            print(f"Error synthesizing results: {str(e)}")
            raise
