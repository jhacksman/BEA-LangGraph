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
        self._raw_routes = routes
        self.routes = {
            name: Route(name=name, keywords=keywords, handler=name)
            for name, keywords in routes.items()
        }
        
    @property
    def raw_routes(self) -> Dict[str, List[str]]:
        """Get raw route definitions for testing."""
        return self._raw_routes
        
    async def route(self, text: str) -> str:
        """Route text to appropriate handler based on keywords.
        
        Args:
            text: Input text to classify
            
        Returns:
            Handler name for the matched route or 'default'
        """
        text = text.lower()
        
        # Try exact matches first
        for route in self.routes.values():
            for keyword in route.all_keywords:
                if f" {keyword} " in f" {text} ":
                    return route.name
        
        # Try partial matches as fallback
        for route in self.routes.values():
            for keyword in route.all_keywords:
                if keyword in text:
                    return route.name
        
        return 'default'
