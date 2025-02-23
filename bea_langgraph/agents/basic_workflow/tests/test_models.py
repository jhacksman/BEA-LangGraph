"""Tests for document workflow state models."""

import pytest
from ..models import DocumentState, WorkflowConfig

def test_document_state_creation():
    """Test document state initialization."""
    state = DocumentState(content="test content")
    assert state.content == "test content"
    assert state.metadata == {}
    assert state.review_feedback is None
    assert state.revision_history == []

def test_document_state_feedback():
    """Test adding review feedback."""
    state = DocumentState(content="test content")
    state.add_feedback("needs improvement")
    assert state.review_feedback == ["needs improvement"]

def test_document_state_revision():
    """Test adding document revision."""
    state = DocumentState(content="original")
    state.add_revision("revised")
    assert state.content == "revised"
    assert state.revision_history == ["original"]

def test_workflow_config_validation():
    """Test workflow configuration validation."""
    with pytest.raises(ValueError):
        WorkflowConfig(criteria=[], max_revisions=0)
    
    config = WorkflowConfig(
        criteria=["clarity", "conciseness"],
        max_revisions=3,
        require_approval=True
    )
    assert config.max_revisions == 3
    assert len(config.criteria) == 2
