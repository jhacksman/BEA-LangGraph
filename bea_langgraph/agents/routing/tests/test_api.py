"""Tests for routing agent API components."""

import os
import pytest
from ..api.client import RoutingClient
from ..api.handlers import RoutingResponseHandler

@pytest.mark.asyncio
async def test_routing_client():
    """Test routing client functionality."""
    # Mock client for testing
    class MockRoutingClient:
        def __init__(self):
            self.base_url = "https://api.venice.ai/api/v1"
            self.headers = {"Authorization": f"Bearer test_key"}
            
        async def stream_completion(self, messages, **kwargs):
            if "technical" in str(messages).lower():
                yield "Route: technical_review\nReasoning: Contains technical terms."
            elif "billing" in str(messages).lower():
                yield "Route: billing\nReasoning: Payment related query."
            else:
                yield "Route: general\nReasoning: General inquiry."
            
    client = MockRoutingClient()
    
    input_text = "Process this document for technical review"
    routes_desc = """
    Route: technical_review
    Description: Technical document review and feedback
    Criteria: technical content, code review, documentation review
    
    Route: content_edit
    Description: General content editing and improvement
    Criteria: grammar, style, clarity, formatting
    """
    
    chunks = []
    async for chunk in client.get_route_analysis(input_text, routes_desc):
        chunks.append(chunk)
        
    assert len(chunks) > 0
    assert any("<think>" in chunk for chunk in chunks)

def test_routing_handler():
    """Test routing response handler."""
    handler = RoutingResponseHandler()
    
    # Test think tag processing
    handler.process_chunk("<think>Analyzing technical aspects of the request</think>")
    assert len(handler.reasoning) == 1
    assert "technical aspects" in handler.reasoning[0]
    
    # Test route selection
    handler.process_chunk("Selected Route: technical_review\nThis is clearly the best match.")
    assert handler.route == "technical_review"
    assert handler.confidence > 0.7  # High confidence due to "clearly"
    
    # Test uncertainty handling
    handler = RoutingResponseHandler()
    handler.process_chunk("Selected Route: content_edit\nThis might be appropriate.")
    assert handler.route == "content_edit"
    assert handler.confidence < 0.7  # Lower confidence due to "might"
