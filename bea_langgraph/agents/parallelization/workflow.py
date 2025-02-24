"""
Parallelization workflow implementation.

This module implements the parallelization pattern from Anthropic's research,
providing functionality for parallel task processing and result aggregation.
"""

import asyncio
from typing import List, Dict, Any, Optional
from .models import ParallelTask, ParallelResult, ParallelConfig
from ..basic_workflow.api.client import VeniceClient

class ParallelWorkflow:
    """Implementation of parallel processing workflow."""
    
    def __init__(self, config: ParallelConfig, client: VeniceClient):
        """Initialize workflow with configuration and API client."""
        self.config = config
        self.client = client
        
    async def process_tasks(self, tasks: List[ParallelTask]) -> ParallelResult:
        """Process multiple tasks in parallel."""
        try:
            # Process tasks concurrently with semaphore for control
            sem = asyncio.Semaphore(self.config.max_concurrent_tasks)
            async with sem:
                results = await asyncio.gather(
                    *[self._process_task(task) for task in tasks],
                    return_exceptions=True
                )
            
            # Handle results and exceptions
            processed_tasks = []
            for task, result in zip(tasks, results):
                if isinstance(result, Exception):
                    print(f"Error processing task {task.task_id}: {str(result)}")
                    task.result = f"Error: {str(result)}"
                else:
                    task.result = result
                processed_tasks.append(task)
            
            # Aggregate results
            combined_result = await self._aggregate_results(processed_tasks)
            return ParallelResult(
                tasks=processed_tasks,
                combined_result=combined_result
            )
            
        except Exception as e:
            print(f"Error in parallel processing: {str(e)}")
            raise
            
    async def _process_task(self, task: ParallelTask) -> str:
        """Process a single task with timeout."""
        try:
            async with asyncio.timeout(self.config.timeout_per_task):
                messages = [
                    {"role": "system", "content": "Process this task efficiently and accurately."},
                    {"role": "user", "content": task.content}
                ]
                
                result_buffer = []
                async for chunk in self.client.stream_completion(messages):
                    if chunk.startswith("<think>"):
                        print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                        continue
                    result_buffer.append(chunk)
                    
                return "".join(result_buffer)
                
        except asyncio.TimeoutError:
            raise Exception(f"Task {task.task_id} timed out")
        except Exception as e:
            raise Exception(f"Error processing task {task.task_id}: {str(e)}")
            
    async def _aggregate_results(self, tasks: List[ParallelTask]) -> str:
        """Aggregate results based on configured strategy."""
        if self.config.aggregation_strategy == "concatenate":
            return "\n\n".join(task.result for task in tasks if task.result)
        else:
            raise ValueError(f"Unknown aggregation strategy: {self.config.aggregation_strategy}")
