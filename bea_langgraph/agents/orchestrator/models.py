"""
Models for orchestrator-workers pattern.

This module implements the orchestrator-workers pattern from Anthropic's research,
providing models for task breakdown, delegation, and result synthesis.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SubTask(BaseModel):
    """Model for a subtask that can be delegated to workers."""
    task_id: str
    description: str
    result: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class Task(BaseModel):
    """Model for a complex task that can be broken down."""
    description: str
    subtasks: List[SubTask] = Field(default_factory=list)
    result: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class OrchestratorConfig(BaseModel):
    """Configuration for orchestrator workflow."""
    max_subtasks: int = Field(default=5, ge=1)
    timeout_per_subtask: float = Field(default=30.0, ge=0.0)
    synthesis_timeout: float = Field(default=60.0, ge=0.0)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
