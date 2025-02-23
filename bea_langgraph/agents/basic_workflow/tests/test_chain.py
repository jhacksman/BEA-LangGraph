"""Tests for document workflow chain implementation."""

import pytest
from ..chain import DocumentWorkflow
from ..models import WorkflowConfig, DocumentState
from ..api.client import VeniceClient

@pytest.fixture
def workflow():
    """Create a test workflow."""
    config = WorkflowConfig(
        criteria=["clarity", "conciseness"],
        max_revisions=2
    )
    client = VeniceClient("test_key")
    return DocumentWorkflow(config, client)

@pytest.mark.asyncio
async def test_document_generation(workflow):
    """Test document generation step."""
    initial_state = {
        "document": DocumentState(content=""),
        "config": workflow.config
    }
    
    result = await workflow.run(initial_state)
    assert isinstance(result["document"], DocumentState)
    assert result["document"].content != ""

@pytest.mark.asyncio
async def test_review_process(workflow):
    """Test document review step."""
    initial_state = {
        "document": DocumentState(content="test document"),
        "config": workflow.config
    }
    
    result = await workflow.run(initial_state)
    assert result["document"].review_feedback is not None
    assert len(result["document"].review_feedback) > 0

@pytest.mark.asyncio
async def test_revision_workflow(workflow):
    """Test complete revision workflow."""
    initial_state = {
        "document": DocumentState(content="initial content"),
        "config": workflow.config
    }
    
    result = await workflow.run(initial_state)
    assert len(result["document"].revision_history) > 0
    assert result["document"].content != "initial content"

@pytest.mark.asyncio
async def test_max_revisions(workflow):
    """Test max revisions limit."""
    initial_state = {
        "document": DocumentState(content="test"),
        "config": workflow.config
    }
    
    result = await workflow.run(initial_state)
    assert len(result["document"].revision_history) <= workflow.config.max_revisions
