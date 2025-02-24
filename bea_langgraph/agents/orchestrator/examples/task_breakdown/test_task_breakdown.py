"""Tests for complex task breakdown example."""

import pytest
from ..task_breakdown.workflow import TaskBreakdownWorkflow
from ...models import OrchestratorConfig
from ....basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_complex_task_processing():
    """Test processing of complex task."""
    config = OrchestratorConfig(max_subtasks=3)
    client = VeniceClient(api_key="test_key")
    workflow = TaskBreakdownWorkflow(config, client)
    
    task = "Analyze the impact of AI on different industries and provide recommendations."
    result = await workflow.process_complex_task(task)
    
    assert result
    assert len(result.split("\n")) >= 3  # Should have multiple sections

@pytest.mark.asyncio
async def test_task_breakdown():
    """Test task breakdown into subtasks."""
    config = OrchestratorConfig(max_subtasks=2)
    client = VeniceClient(api_key="test_key")
    workflow = TaskBreakdownWorkflow(config, client)
    
    task = "Write a comprehensive report on renewable energy."
    result = await workflow.process_complex_task(task)
    
    assert result
    assert len(result.split("\n")) <= config.max_subtasks * 2  # Reasonable size
