"""Models for routing workflow implementation."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Route(BaseModel):
    """Simple route definition with keywords for classification."""
    name: str = Field(..., min_length=1)
    keywords: List[str] = Field(..., min_items=1)
    handler: Optional[str] = Field(default=None)
    
    @property
    def all_keywords(self) -> List[str]:
        """Get all keywords including variations."""
        variations = []
        for kw in self.keywords:
            variations.append(kw.lower())
            if " " in kw:  # Add variations without spaces
                variations.append(kw.lower().replace(" ", ""))
        return variations
