"""Tests for result synthesis example."""

import pytest
from ..synthesis.workflow import SynthesisWorkflow
from ...models import OrchestratorConfig
from ....basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_result_synthesis():
    """Test synthesis of multiple results."""
    config = OrchestratorConfig(max_subtasks=3)
    client = VeniceClient(api_key="test_key")
    workflow = SynthesisWorkflow(config, client)
    
    results = [
        "AI shows promise in healthcare diagnostics",
        "Implementation costs remain a challenge",
        "Staff training needs are significant"
    ]
    context = "Healthcare AI adoption analysis"
    
    result = await workflow.synthesize_results(results, context)
    
    assert result
    assert all(r.lower() in result.lower() for r in ["healthcare", "cost", "training"])

@pytest.mark.asyncio
async def test_synthesis_with_errors():
    """Test synthesis with some error results."""
    config = OrchestratorConfig(max_subtasks=3)
    client = VeniceClient(api_key="test_key")
    workflow = SynthesisWorkflow(config, client)
    
    results = [
        "Valid result 1",
        "Error: Failed to process",
        "Valid result 2"
    ]
    context = "Test context"
    
    result = await workflow.synthesize_results(results, context)
    
    assert result
    assert "valid" in result.lower()
    assert "error" not in result.lower()
