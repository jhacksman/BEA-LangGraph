"""Tests for content improvement example."""

import pytest
from ..improvement.workflow import ImprovementWorkflow
from ...models import EvaluatorConfig
from ....basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_content_improvement():
    """Test iterative content improvement."""
    config = EvaluatorConfig(max_iterations=3)
    client = VeniceClient(api_key="test_key")
    workflow = ImprovementWorkflow(config, client)
    
    content = "Initial test content"
    criteria = ["clarity", "completeness"]
    target_score = 0.9
    
    improved_content, history = await workflow.improve_content(content, criteria, target_score)
    
    assert improved_content != content
    assert len(history) > 0
    assert all(e.score for e in history)
    assert history[-1].score >= history[0].score

@pytest.mark.asyncio
async def test_improvement_limit():
    """Test improvement iteration limit."""
    config = EvaluatorConfig(max_iterations=2)
    client = VeniceClient(api_key="test_key")
    workflow = ImprovementWorkflow(config, client)
    
    content = "Test content"
    criteria = ["clarity"]
    target_score = 1.0  # Unreachable target
    
    improved_content, history = await workflow.improve_content(content, criteria, target_score)
    
    assert len(history) <= config.max_iterations
    assert improved_content != content
