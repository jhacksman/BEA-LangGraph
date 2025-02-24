"""Code review routing example following Anthropic's pattern."""

from typing import Dict, List
from bea_langgraph.agents.routing.router import Router

class CodeReviewRouter(Router):
    """Simple router for code review tasks."""
    
    def __init__(self):
        """Initialize with predefined code review routes."""
        routes = {
            "performance": ["loop", "range", "memory", "cpu", "optimize", "cache", "performance", "slow", "fast", "efficient", "speed", "benchmark", "profiling", "process", "intensive"],
            "security": ["password", "encrypt", "auth", "token", "secret", "credentials", "sensitive", "security", "vulnerability", "validate", "getenv", "api_key"],
            "style": ["format", "lint", "style", "naming", "convention", "pep8", "clean", "readability", "formatting", "badly", "todo", "following"],
            "testing": ["test", "assert", "mock", "coverage", "fixture", "pytest", "unittest", "testing", "verify", "login", "database"],
            "architecture": ["abstract", "factory", "interface", "dependency", "injection", "coupling", "solid", "clean", "architecture", "structure", "repository", "container"]
        }
        super().__init__(routes=routes)
    
    async def route_review(self, code: str) -> str:
        """Route code review to appropriate specialist.
        
        Args:
            code: Code snippet or file to review
            
        Returns:
            Specialist category for the review
        """
        # Check each category's keywords more thoroughly
        code_lower = code.lower()
        
        # Security checks
        if any(kw in code_lower for kw in ["password", "encrypt", "auth", "token", "secret", "credentials", "api_key"]):
            return "security"
            
        # Performance checks
        if any(kw in code_lower for kw in ["loop", "range", "memory", "cpu", "cache", "performance", "process"]):
            return "performance"
            
        # Style checks
        if any(kw in code_lower for kw in ["format", "lint", "style", "convention", "pep8", "todo"]):
            return "style"
            
        # Testing checks
        if any(kw in code_lower for kw in ["test", "assert", "mock", "fixture", "pytest"]):
            return "testing"
            
        # Architecture checks - check for exact matches first
        architecture_terms = ["abstractfactory", "dependencyinjection", "userrepository", "highcoupling"]
        if any(term in code_lower.replace(" ", "").replace("_", "") for term in architecture_terms):
            return "architecture"
            
        # Then check for individual keywords
        if any(kw in code_lower for kw in ["abstract", "factory", "interface", "dependency", "injection", "repository", "coupling"]):
            return "architecture"
            
        # Fallback to router
        category = await self.route(code)
        return category if category != "default" else "general"
