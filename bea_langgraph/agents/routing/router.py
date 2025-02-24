"""Router implementation following Anthropic's routing workflow pattern."""

from typing import List
from .models import Route, RouterConfig

class Router:
    """Simple router that classifies input and directs to specialized handlers."""
    
    def __init__(self, routes: List[Route], default_handler: str):
        """Initialize router with routes and default handler."""
        self.routes = routes
        self.default_handler = default_handler
        
    async def route(self, input_text: str) -> str:
        """Route input to appropriate handler based on classification."""
        # Simple classification and routing
        for route in self.routes:
            if self._matches_criteria(input_text, route.criteria):
                return route.handler
        return self.default_handler
        
    def _matches_criteria(self, input_text: str, criteria: List[str]) -> bool:
        """Check if input matches route criteria."""
        input_lower = input_text.lower()
        return any(keyword.lower() in input_lower for keyword in criteria)
