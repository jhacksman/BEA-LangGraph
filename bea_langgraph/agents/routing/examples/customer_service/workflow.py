"""Customer service routing example following Anthropic's pattern."""

from typing import Dict, List
from ...router import Router

class CustomerServiceRouter(Router):
    """Simple router for customer service queries."""
    
    def __init__(self):
        """Initialize with predefined customer service routes."""
        routes = {
            "technical": ["error", "bug", "not working", "broken", "failed"],
            "billing": ["charge", "payment", "refund", "invoice", "subscription"],
            "account": ["login", "password", "access", "account", "profile"],
            "product": ["feature", "how to", "usage", "documentation", "help"]
        }
        super().__init__(routes=routes)
    
    async def route_query(self, query: str) -> str:
        """Route customer query to appropriate department.
        
        Args:
            query: Customer service query
            
        Returns:
            Department name for handling the query
        """
        department = await self.route(query)
        return department if department != "default" else "general"
