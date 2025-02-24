"""Tests for multi-agent voting example."""

import pytest
from ..voting.workflow import VotingWorkflow
from ...models import ParallelConfig
from ....basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_voting_consensus():
    """Test basic voting consensus workflow."""
    config = ParallelConfig(max_concurrent_tasks=3)
    client = VeniceClient(api_key="test_key")
    workflow = VotingWorkflow(config, client)
    
    question = "What is the best approach for this problem?"
    result = await workflow.get_consensus(question, num_voters=3)
    
    assert result
    assert "Consensus:" in result
    assert "Votes:" in result

@pytest.mark.asyncio
async def test_voting_error_handling():
    """Test voting with failed votes."""
    config = ParallelConfig(timeout_per_task=0.1)  # Short timeout to trigger errors
    client = VeniceClient(api_key="test_key")
    workflow = VotingWorkflow(config, client)
    
    question = "What is the best approach?"
    result = await workflow.get_consensus(question, num_voters=3)
    
    assert result
    assert "No consensus" in result
