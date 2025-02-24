"""Customer service routing example following Anthropic's pattern."""

from typing import Dict, List
from bea_langgraph.agents.routing.router import Router

class CustomerServiceRouter(Router):
    """Simple router for customer service queries."""
    
    def __init__(self):
        """Initialize with predefined customer service routes."""
        routes = {
            "billing": ["charge", "payment", "refund", "invoice", "subscription", "bill", "money", "cost", "price", "pay", "paid", "billing"],
            "technical": ["error", "bug", "not working", "broken", "failed", "issue", "problem", "crash", "fix", "technical"],
            "account": ["login", "password", "access", "account", "profile", "sign in", "register", "credentials"],
            "product": ["feature", "how to", "usage", "documentation", "help", "guide", "tutorial", "learn"]
        }
        super().__init__(routes=routes)
    
    async def route_query(self, query: str) -> str:
        """Route customer query to appropriate department.
        
        Args:
            query: Customer service query
            
        Returns:
            Department name for handling the query
        """
        # Check for product queries first
        product_terms = ["how to", "feature", "usage", "documentation", "help", "guide", "tutorial", "learn"]
        if any(term in query.lower() for term in product_terms):
            return "product"
            
        # Check for general queries
        general_terms = ["general", "hello", "hi", "question", "inquiry", "feedback"]
        if any(term in query.lower() for term in general_terms):
            return "general"
            
        department = await self.route(query)
        return department if department != "default" else "general"
