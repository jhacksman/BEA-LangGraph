"""Mock API client for testing."""

class MockVeniceClient:
    """Mock Venice API client for testing."""
    
    def __init__(self):
        self.base_url = "https://api.venice.ai/api/v1"
        self.headers = {"Authorization": f"Bearer test_key"}
        
    async def stream_completion(self, messages, **kwargs):
        """Mock streaming completion."""
        if "error" in str(messages):
            raise Exception("Test error")
        yield "Test response"
