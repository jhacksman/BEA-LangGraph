"""
Multi-agent voting example using parallelization pattern.

This example demonstrates using parallel processing to get multiple agent opinions
and aggregate them through voting.
"""

import asyncio
from typing import List, Dict, Any
from ...models import ParallelTask, ParallelConfig, ParallelResult
from ...workflow import ParallelWorkflow
from ....basic_workflow.api.client import VeniceClient

class VotingWorkflow(ParallelWorkflow):
    """Implementation of multi-agent voting workflow."""
    
    async def get_consensus(self, question: str, num_voters: int = 3) -> str:
        """Get consensus through parallel agent voting."""
        # Create voting tasks
        tasks = [
            ParallelTask(
                task_id=f"voter_{i}",
                content=f"As an independent agent, evaluate this question and provide your answer:\n\n{question}"
            )
            for i in range(num_voters)
        ]
        
        # Get votes in parallel
        result = await self.process_tasks(tasks)
        
        # Determine consensus
        consensus = await self._determine_consensus(result.tasks)
        return consensus
        
    async def _determine_consensus(self, tasks: List[ParallelTask]) -> str:
        """Determine consensus from multiple votes."""
        # Simple majority voting, could be more sophisticated
        votes = [task.result for task in tasks if task.result]
        if not votes:
            return "No consensus reached - no valid votes"
            
        # Count occurrences of each vote
        vote_counts = {}
        for vote in votes:
            vote_counts[vote] = vote_counts.get(vote, 0) + 1
            
        # Find majority
        majority_vote = max(vote_counts.items(), key=lambda x: x[1])[0]
        return f"Consensus: {majority_vote} (Votes: {vote_counts})"
