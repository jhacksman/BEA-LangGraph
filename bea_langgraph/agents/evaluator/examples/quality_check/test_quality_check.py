"""Tests for content quality check example."""

import pytest
from ..quality_check.workflow import QualityCheckWorkflow
from ...models import EvaluatorConfig
from ....basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_quality_check():
    """Test basic quality check workflow."""
    config = EvaluatorConfig(threshold=0.8)
    client = VeniceClient(api_key="test_key")
    workflow = QualityCheckWorkflow(config, client)
    
    content = "Test content for quality check"
    criteria = ["clarity", "accuracy", "completeness"]
    
    evaluation = await workflow.check_quality(content, criteria)
    
    assert evaluation.score >= 0.0
    assert evaluation.score <= 1.0
    assert evaluation.metadata["quality_report"]
    assert "recommendation" in evaluation.metadata["quality_report"]

@pytest.mark.asyncio
async def test_quality_report():
    """Test quality report generation."""
    config = EvaluatorConfig(threshold=0.9)
    client = VeniceClient(api_key="test_key")
    workflow = QualityCheckWorkflow(config, client)
    
    content = "High quality test content with clear structure and accurate information"
    criteria = ["clarity", "accuracy"]
    
    evaluation = await workflow.check_quality(content, criteria)
    report = evaluation.metadata["quality_report"]
    
    assert "score" in report
    assert "strengths" in report
    assert "areas_for_improvement" in report
    assert "recommendation" in report
    assert report["recommendation"] in ["Accept", "Needs Revision"]
