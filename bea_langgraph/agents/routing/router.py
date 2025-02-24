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
        self.routes = {
            name: Route(name=name, keywords=keywords, handler=name)
            for name, keywords in routes.items()
        }
        
    async def route(self, text: str) -> str:
        """Route text to appropriate handler based on keywords.
        
        Args:
            text: Input text to classify
            
        Returns:
            Handler name for the matched route or 'default'
        """
        text = f" {text.lower()} "  # Add spaces for word boundary checks
        
        # Try exact phrase matches first
        for route in self.routes.values():
            for keyword in route.keywords:
                keyword = keyword.lower()
                if " " in keyword:  # Multi-word keyword
                    if keyword in text:
                        return route.name
                else:  # Single word with boundaries
                    if f" {keyword} " in text:
                        return route.name
        
        # Try partial matches as fallback
        for route in self.routes.values():
            for keyword in route.keywords:
                if keyword.lower() in text:
                    return route.name
        
        return 'default'
