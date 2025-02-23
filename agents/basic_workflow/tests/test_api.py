"""Tests for venice.ai API client and think tag handling."""

import pytest
from ..api.client import VeniceClient
from ..api.handlers import ThinkTagHandler

@pytest.fixture
def api_client():
    """Create a test API client."""
    return VeniceClient("test_key")

@pytest.fixture
def think_handler():
    """Create a test think tag handler."""
    return ThinkTagHandler()

def test_think_tag_handling():
    """Test think tag processing."""
    handler = ThinkTagHandler()
    
    # Test start of think section
    chunk1 = 'data: {"choices":[{"delta":{"content":"<think>"}}]}'
    assert handler.process_chunk(chunk1) is None
    
    # Test think content
    chunk2 = 'data: {"choices":[{"delta":{"content":"reasoning"}}]}'
    assert handler.process_chunk(chunk2) is None
    
    # Test end of think section
    chunk3 = 'data: {"choices":[{"delta":{"content":"</think>"}}]}'
    assert handler.process_chunk(chunk3) is None
    
    # Test regular content
    chunk4 = 'data: {"choices":[{"delta":{"content":"actual content"}}]}'
    assert handler.process_chunk(chunk4) == "actual content"
    
    # Verify think content
    assert handler.get_think_content() == "reasoning"

@pytest.mark.asyncio
async def test_stream_completion(api_client, monkeypatch):
    """Test streaming completion with think tag handling."""
    class MockResponse:
        status = 200
        async def content(self):
            yield b'data: {"choices":[{"delta":{"content":"<think>reasoning</think>"}}]}\n'
            yield b'data: {"choices":[{"delta":{"content":"test content"}}]}\n'
            yield b'data: [DONE]\n'
        
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
    
    class MockAsyncContextManager:
        def __init__(self, response):
            self.response = response

        async def __aenter__(self):
            return self.response

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    async def mock_post(*args, **kwargs):
        return MockAsyncContextManager(MockResponse())
    
    import aiohttp
    monkeypatch.setattr(aiohttp.ClientSession, "post", mock_post)
    
    messages = [
        {"role": "user", "content": "test prompt"}
    ]
    
    chunks = []
    async for chunk in api_client.stream_completion(messages):
        if not chunk.startswith("__THINK__"):
            chunks.append(chunk)
    
    assert len(chunks) == 1
    assert chunks[0] == "test content"
