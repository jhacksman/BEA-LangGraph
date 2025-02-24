"""Models for routing workflow implementation."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Route(BaseModel):
    """Simple route definition with keywords for classification."""
    name: str
    keywords: List[str]
    handler: Optional[str] = Field(default=None)
