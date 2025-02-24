"""Models for routing workflow implementation."""

from typing import List
from pydantic import BaseModel

class Route(BaseModel):
    """Represents a route with its handler and criteria."""
    name: str
    description: str
    criteria: List[str]
    handler: str

class RouterConfig(BaseModel):
    """Configuration for the routing workflow."""
    routes: List[Route]
    default_handler: str
