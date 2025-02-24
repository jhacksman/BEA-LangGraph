"""
Content quality check example using evaluator-optimizer pattern.

This example demonstrates using the evaluator pattern to check content quality
against specific criteria.
"""

from typing import List, Dict, Any, Tuple
from ...models import EvaluationResult, EvaluatorConfig
from ...workflow import EvaluatorWorkflow
from ....basic_workflow.api.client import VeniceClient

class QualityCheckWorkflow(EvaluatorWorkflow):
    """Implementation of content quality check workflow."""
    
    async def check_quality(self, content: str, quality_criteria: List[str]) -> EvaluationResult:
        """Check content quality against specific criteria."""
        # Evaluate content without improvement
        evaluation = await self._evaluate(content, quality_criteria)
        
        # Provide detailed quality report
        report = self._generate_quality_report(evaluation)
        evaluation.metadata["quality_report"] = report
        
        return evaluation
        
    def _generate_quality_report(self, evaluation: EvaluationResult) -> Dict[str, Any]:
        """Generate detailed quality report from evaluation."""
        return {
            "score": evaluation.score,
            "strengths": [f for f in evaluation.feedback if not f.startswith("Needs improvement")],
            "areas_for_improvement": evaluation.improvements,
            "recommendation": "Accept" if evaluation.score >= self.config.threshold else "Needs Revision"
        }
