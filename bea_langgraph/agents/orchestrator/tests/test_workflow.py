"""Tests for orchestrator workflow."""

import pytest
from ..models import Task, SubTask, OrchestratorConfig
from ..workflow import OrchestratorWorkflow
from ...basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_task_execution():
    """Test basic task execution workflow."""
    config = OrchestratorConfig(max_subtasks=2)
    client = VeniceClient(api_key="test_key")
    workflow = OrchestratorWorkflow(config, client)
    
    task = Task(description="Analyze this complex problem and provide solutions.")
    result = await workflow.execute(task)
    
    assert result.subtasks
    assert len(result.subtasks) <= config.max_subtasks
    assert result.result
    assert all(subtask.result for subtask in result.subtasks)

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in task execution."""
    config = OrchestratorConfig(timeout_per_subtask=0.1)  # Short timeout to trigger error
    client = VeniceClient(api_key="test_key")
    workflow = OrchestratorWorkflow(config, client)
    
    task = Task(description="Test task")
    result = await workflow.execute(task)
    
    assert result.subtasks
    assert any("Error" in subtask.result for subtask in result.subtasks)

@pytest.mark.asyncio
async def test_subtask_limit():
    """Test subtask limit enforcement."""
    config = OrchestratorConfig(max_subtasks=2)
    client = VeniceClient(api_key="test_key")
    workflow = OrchestratorWorkflow(config, client)
    
    task = Task(description="A task that could be broken into many subtasks")
    result = await workflow.execute(task)
    
    assert len(result.subtasks) <= config.max_subtasks
