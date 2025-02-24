"""Models for routing workflow implementation."""

from typing import List, Dict
from pydantic import BaseModel

class Route(BaseModel):
    """Simple route definition with keywords for classification."""
    name: str
    keywords: List[str]
    handler: str
