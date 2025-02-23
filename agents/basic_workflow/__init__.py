"""
Basic Workflows pattern implementation using LangGraph.

This module implements document processing workflows following the pattern
described in Anthropic's "Building Effective Agents" research.
"""

from .chain import DocumentWorkflow
from .models import DocumentState, WorkflowConfig

__all__ = ["DocumentWorkflow", "DocumentState", "WorkflowConfig"]
