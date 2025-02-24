"""Tests for document sectioning example."""

import pytest
from ..sectioning.workflow import SectioningWorkflow
from ...models import ParallelConfig
from ....basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_document_sectioning():
    """Test basic document sectioning workflow."""
    config = ParallelConfig(max_concurrent_tasks=2)
    client = VeniceClient(api_key="test_key")
    workflow = SectioningWorkflow(config, client)
    
    document = """Section 1 content.
    
    Section 2 content.
    
    Section 3 content."""
    
    criteria = ["clarity", "conciseness"]
    result = await workflow.process_document(document, criteria)
    
    assert result
    assert len(result.split("\n\n")) >= 3

@pytest.mark.asyncio
async def test_empty_document():
    """Test handling of empty document."""
    config = ParallelConfig(max_concurrent_tasks=2)
    client = VeniceClient(api_key="test_key")
    workflow = SectioningWorkflow(config, client)
    
    document = ""
    criteria = ["clarity"]
    result = await workflow.process_document(document, criteria)
    
    assert result == ""
