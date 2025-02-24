"""Models for routing agent implementation."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Route(BaseModel):
    """Represents a route that can be taken by the router."""
    name: str
    description: str
    criteria: List[str]
    handler: str

class RouterConfig(BaseModel):
    """Configuration for the routing agent."""
    routes: List[Route]
    default_handler: str
    max_retries: int = 3
    confidence_threshold: float = 0.7

class RoutingState(BaseModel):
    """State of the routing process."""
    input: str
    selected_route: Optional[str] = None
    confidence: float = 0.0
    attempts: int = 0
    history: List[Dict[str, Any]] = []

    def add_attempt(self, route: str, confidence: float) -> None:
        """Add a routing attempt to history."""
        self.attempts += 1
        self.history.append({
            "attempt": self.attempts,
            "route": route,
            "confidence": confidence
        })

    def set_route(self, route: str, confidence: float) -> None:
        """Set the selected route and its confidence."""
        self.selected_route = route
        self.confidence = confidence
        self.add_attempt(route, confidence)
