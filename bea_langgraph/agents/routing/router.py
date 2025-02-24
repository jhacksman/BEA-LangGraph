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
        words = text.split()
        matches = {}
        
        for route in self.routes.values():
            score = 0
            for keyword in route.all_keywords:
                keyword = keyword.lower()
                keyword_parts = keyword.split()
                
                # Check for exact phrase matches
                if len(keyword_parts) > 1 and keyword in text:
                    score += 4
                    continue
                
                # Check for exact word matches
                for kw_part in keyword_parts:
                    if kw_part in words:
                        score += 3
                    # Check for word boundary matches
                    elif any(w.startswith(kw_part + " ") or w.endswith(" " + kw_part) or w == kw_part for w in words):
                        score += 2
                    # Check for substring matches
                    elif any(kw_part in w for w in words):
                        score += 1
            
            if score > 0:
                matches[route.name] = matches.get(route.name, 0) + score
        
        if matches:
            # Return route with highest score
            return max(matches.items(), key=lambda x: x[1])[0]
        
        return 'default'
