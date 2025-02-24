"""Code review routing example following Anthropic's pattern."""

from typing import Dict, List
from bea_langgraph.agents.routing.router import Router

class CodeReviewRouter(Router):
    """Simple router for code review tasks."""
    
    def __init__(self):
        """Initialize with predefined code review routes."""
        routes = {
            "security": ["password", "encrypt", "auth", "token", "secret", "credentials", "sensitive"],
            "performance": ["loop", "memory", "cpu", "optimize", "cache", "performance", "slow", "fast", "efficient"],
            "style": ["format", "lint", "style", "naming", "convention", "pep8", "clean"],
            "testing": ["test", "assert", "mock", "coverage", "fixture", "pytest", "unittest"],
            "architecture": ["pattern", "design", "interface", "dependency", "coupling", "solid", "clean"]
        }
        super().__init__(routes=routes)
    
    async def route_review(self, code: str) -> str:
        """Route code review to appropriate specialist.
        
        Args:
            code: Code snippet or file to review
            
        Returns:
            Specialist category for the review
        """
        category = await self.route(code)
        return category if category != "default" else "general"
