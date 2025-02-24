"""
Models for parallelization workflow pattern.

This module implements the parallelization pattern from Anthropic's research,
providing models for parallel task processing and result aggregation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ParallelTask(BaseModel):
    """Model for a task that can be processed in parallel."""
    task_id: str
    content: str
    result: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class ParallelResult(BaseModel):
    """Model for aggregated results from parallel tasks."""
    tasks: List[ParallelTask]
    combined_result: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class ParallelConfig(BaseModel):
    """Configuration for parallel processing workflow."""
    max_concurrent_tasks: int = Field(default=5, ge=1)
    timeout_per_task: float = Field(default=30.0, ge=0.0)
    aggregation_strategy: str = Field(default="concatenate")
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
