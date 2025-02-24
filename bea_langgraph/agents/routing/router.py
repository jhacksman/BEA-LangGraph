"""Router implementation following Anthropic's routing workflow pattern."""

from typing import List, Dict
from .models import Route

class Router:
    """Simple router that classifies input based on keywords."""
    
    def __init__(self, routes: Dict[str, List[str]]):
        """Initialize router with route definitions.
        
        Args:
            routes: Dictionary mapping handler names to their keywords
        """
        self.routes = routes
        
    async def route(self, text: str) -> str:
        """Route text to appropriate handler based on keywords.
        
        Args:
            text: Input text to classify
            
        Returns:
            Handler name for the matched route or 'default'
        """
        text = text.lower()
        for handler, keywords in self.routes.items():
            if any(kw.lower() in text for kw in keywords):
                return handler
        return 'default'
