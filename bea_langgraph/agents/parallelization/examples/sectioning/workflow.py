"""
Document sectioning example using parallelization pattern.

This example demonstrates using parallel processing to handle document sections
independently and then combining the results.
"""

import asyncio
from typing import List, Dict, Any
from ...models import ParallelTask, ParallelConfig, ParallelResult
from ...workflow import ParallelWorkflow
from ....basic_workflow.api.client import VeniceClient

class SectioningWorkflow(ParallelWorkflow):
    """Implementation of document sectioning workflow."""
    
    async def process_document(self, document: str, section_criteria: List[str]) -> str:
        """Process document by sections in parallel."""
        # Split document into sections
        sections = self._split_into_sections(document)
        
        # Create tasks for each section
        tasks = [
            ParallelTask(
                task_id=f"section_{i}",
                content=f"Process this section following criteria: {', '.join(section_criteria)}\n\nSection:\n{section}"
            )
            for i, section in enumerate(sections)
        ]
        
        # Process sections in parallel
        result = await self.process_tasks(tasks)
        return result.combined_result
        
    def _split_into_sections(self, document: str) -> List[str]:
        """Split document into processable sections."""
        # Simple split by double newline, could be more sophisticated
        sections = [s.strip() for s in document.split("\n\n") if s.strip()]
        return sections
