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
        text = f" {text.lower()} "
        matches = {}
        
        # Try exact matches first
        for route in self.routes.values():
            for keyword in route.all_keywords:
                if f" {keyword} " in text:
                    matches[route.name] = matches.get(route.name, 0) + 2
                elif keyword in text:
                    matches[route.name] = matches.get(route.name, 0) + 1
        
        if matches:
            # Return route with most matches
            return max(matches.items(), key=lambda x: x[1])[0]
        
        return 'default'
