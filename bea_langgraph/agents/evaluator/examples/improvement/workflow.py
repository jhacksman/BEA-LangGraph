"""
Content improvement example using evaluator-optimizer pattern.

This example demonstrates using the evaluator pattern to iteratively improve
content quality.
"""

from typing import List, Dict, Any, Tuple
from ...models import EvaluationResult, EvaluatorConfig
from ...workflow import EvaluatorWorkflow
from ....basic_workflow.api.client import VeniceClient

class ImprovementWorkflow(EvaluatorWorkflow):
    """Implementation of content improvement workflow."""
    
    async def improve_content(self, content: str, quality_criteria: List[str], target_score: float = 0.9) -> Tuple[str, List[EvaluationResult]]:
        """Improve content until it meets target quality score."""
        # Configure for target score
        self.config.threshold = target_score
        
        # Track improvement history
        history = []
        current_content = content
        
        while len(history) < self.config.max_iterations:
            # Evaluate and improve
            improved_content, evaluation = await self.evaluate_and_improve(current_content, quality_criteria)
            history.append(evaluation)
            
            # Check if target reached
            if evaluation.score >= target_score:
                break
                
            current_content = improved_content
            
        return current_content, history
        
    async def _improve(self, content: str, evaluation: EvaluationResult, criteria: List[str]) -> str:
        """Enhanced improvement with focus on specific criteria."""
        # Prepare improvement context with criteria focus
        improvements_text = "\n".join(
            f"- {improvement} (related to {criterion})"
            for improvement, criterion in zip(evaluation.improvements, criteria)
        )
        
        messages = [
            {"role": "system", "content": """Improve this content focusing specifically on the
            provided criteria. Make targeted improvements that directly address the feedback."""},
            {"role": "user", "content": f"""Content to improve:\n{content}
            
            Current Score: {evaluation.score}
            Target Criteria:\n{', '.join(criteria)}
            Required Improvements:\n{improvements_text}"""}
        ]
        
        result_buffer = []
        async for chunk in self.client.stream_completion(messages):
            if chunk.startswith("<think>"):
                print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                continue
            result_buffer.append(chunk)
            
        return "".join(result_buffer)
