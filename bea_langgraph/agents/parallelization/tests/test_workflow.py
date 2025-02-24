"""Tests for parallelization workflow."""

import pytest
from ..models import ParallelTask, ParallelConfig
from ..workflow import ParallelWorkflow
from ...basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_parallel_processing():
    """Test basic parallel task processing."""
    config = ParallelConfig(max_concurrent_tasks=2)
    client = VeniceClient(api_key="test_key")
    workflow = ParallelWorkflow(config, client)
    
    tasks = [
        ParallelTask(task_id="1", content="Task 1 content"),
        ParallelTask(task_id="2", content="Task 2 content")
    ]
    
    result = await workflow.process_tasks(tasks)
    assert len(result.tasks) == 2
    assert all(task.result for task in result.tasks)
    assert result.combined_result

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in parallel processing."""
    config = ParallelConfig(timeout_per_task=0.1)  # Short timeout to trigger error
    client = VeniceClient(api_key="test_key")
    workflow = ParallelWorkflow(config, client)
    
    tasks = [
        ParallelTask(task_id="1", content="Task 1 content"),
        ParallelTask(task_id="2", content="Task 2 content")
    ]
    
    result = await workflow.process_tasks(tasks)
    assert len(result.tasks) == 2
    assert any("Error" in task.result for task in result.tasks)

@pytest.mark.asyncio
async def test_concurrent_limit():
    """Test concurrent task limit."""
    config = ParallelConfig(max_concurrent_tasks=1)
    client = VeniceClient(api_key="test_key")
    workflow = ParallelWorkflow(config, client)
    
    tasks = [
        ParallelTask(task_id=str(i), content=f"Task {i} content")
        for i in range(3)
    ]
    
    result = await workflow.process_tasks(tasks)
    assert len(result.tasks) == 3
    assert all(task.result for task in result.tasks)
