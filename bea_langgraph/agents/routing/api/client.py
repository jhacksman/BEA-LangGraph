"""Venice.ai API client for routing agent."""

from typing import Dict, Any, AsyncGenerator
from ...basic_workflow.api.client import VeniceClient

class RoutingClient(VeniceClient):
    """Extended Venice.ai client with routing-specific functionality."""
    
    async def get_route_analysis(self, input_text: str, routes_desc: str) -> AsyncGenerator[str, None]:
        """Get route analysis from the model."""
        messages = [
            {
                "role": "system",
                "content": "You are a routing assistant. Analyze the input and select the most appropriate route."
            },
            {
                "role": "user",
                "content": f"""Analyze this input and select the most appropriate route:

Input:
{input_text}

Available Routes:
{routes_desc}

Explain your reasoning and selection."""
            }
        ]
        
        async for chunk in self.stream_completion(messages):
            yield chunk
