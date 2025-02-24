"""
Models for evaluator-optimizer pattern.

This module implements the evaluator-optimizer pattern from Anthropic's research,
providing models for content evaluation and iterative improvement.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    """Model for evaluation results."""
    score: float = Field(ge=0.0, le=1.0)
    feedback: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class EvaluatorConfig(BaseModel):
    """Configuration for evaluator workflow."""
    threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    max_iterations: int = Field(default=3, ge=1)
    timeout_per_evaluation: float = Field(default=30.0, ge=0.0)
    timeout_per_improvement: float = Field(default=60.0, ge=0.0)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
