"""Tests for evaluator workflow."""

import pytest
from ..models import EvaluatorConfig, EvaluationResult
from ..workflow import EvaluatorWorkflow
from ...basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_evaluation():
    """Test basic content evaluation."""
    config = EvaluatorConfig(threshold=0.8)
    client = VeniceClient(api_key="test_key")
    workflow = EvaluatorWorkflow(config, client)
    
    content = "Test content for evaluation"
    criteria = ["clarity", "accuracy"]
    
    result, evaluation = await workflow.evaluate_and_improve(content, criteria)
    
    assert result
    assert isinstance(evaluation, EvaluationResult)
    assert 0.0 <= evaluation.score <= 1.0
    assert evaluation.feedback
    assert evaluation.improvements

@pytest.mark.asyncio
async def test_improvement_cycle():
    """Test improvement cycle with low initial score."""
    config = EvaluatorConfig(
        threshold=0.9,
        max_iterations=2
    )
    client = VeniceClient(api_key="test_key")
    workflow = EvaluatorWorkflow(config, client)
    
    content = "Initial test content"
    criteria = ["clarity", "completeness"]
    
    result, evaluation = await workflow.evaluate_and_improve(content, criteria)
    
    assert result != content  # Content should be improved
    assert evaluation.score > 0.0
    assert len(evaluation.feedback) > 0
    assert len(evaluation.improvements) > 0

@pytest.mark.asyncio
async def test_timeout_handling():
    """Test timeout handling in evaluation."""
    config = EvaluatorConfig(timeout_per_evaluation=0.1)
    client = VeniceClient(api_key="test_key")
    workflow = EvaluatorWorkflow(config, client)
    
    content = "Test content"
    criteria = ["clarity"]
    
    with pytest.raises(Exception):
        await workflow.evaluate_and_improve(content, criteria)
