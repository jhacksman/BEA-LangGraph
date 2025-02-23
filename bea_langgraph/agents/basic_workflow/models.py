"""
Pydantic models for document workflow state management.

This module defines the data models used to track document state and workflow
configuration throughout the processing pipeline.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DocumentState(BaseModel):
    """State model for tracking document processing progress."""
    content: str
    metadata: Dict = Field(default_factory=dict)
    review_feedback: Optional[List[str]] = None
    revision_history: List[str] = Field(default_factory=list)
    
    def add_feedback(self, feedback: str) -> None:
        """Add review feedback to the document state."""
        if self.review_feedback is None:
            self.review_feedback = []
        self.review_feedback.append(feedback)
    
    def add_revision(self, content: str) -> None:
        """Add a new revision to the history and update content."""
        self.revision_history.append(self.content)
        self.content = content

class WorkflowConfig(BaseModel):
    """Configuration for document processing workflow."""
    criteria: List[str]
    max_revisions: int = Field(default=3, ge=1)
    require_approval: bool = True
    
    class Config:
        """Pydantic model configuration."""
        validate_assignment = True
