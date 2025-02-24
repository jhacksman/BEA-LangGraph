"""
Evaluator workflow implementation.

This module implements the evaluator-optimizer pattern from Anthropic's research,
providing functionality for content evaluation and iterative improvement.
"""

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from .models import EvaluationResult, EvaluatorConfig
from ..basic_workflow.api.client import VeniceClient

class EvaluatorWorkflow:
    """Implementation of evaluator-optimizer workflow."""
    
    def __init__(self, config: EvaluatorConfig, client: VeniceClient):
        """Initialize workflow with configuration and API client."""
        self.config = config
        self.client = client
        
    async def evaluate_and_improve(self, content: str, criteria: List[str]) -> Tuple[str, EvaluationResult]:
        """Evaluate content and improve if needed."""
        try:
            # Initial evaluation
            evaluation = await self._evaluate(content, criteria)
            
            # Improve content if score is below threshold
            iterations = 0
            current_content = content
            while (evaluation.score < self.config.threshold and 
                   iterations < self.config.max_iterations):
                print(f"\nIteration {iterations + 1}: Score {evaluation.score:.2f}")
                current_content = await self._improve(current_content, evaluation, criteria)
                evaluation = await self._evaluate(current_content, criteria)
                iterations += 1
                
            return current_content, evaluation
            
        except Exception as e:
            print(f"Error in evaluator workflow: {str(e)}")
            raise
            
    async def _evaluate(self, content: str, criteria: List[str]) -> EvaluationResult:
        """Evaluate content against criteria."""
        try:
            messages = [
                {"role": "system", "content": """Evaluate this content against the provided criteria.
                Provide a score between 0.0 and 1.0, specific feedback, and suggested improvements."""},
                {"role": "user", "content": f"Content to evaluate:\n{content}\n\nCriteria:\n{', '.join(criteria)}"}
            ]
            
            result_buffer = []
            async with asyncio.timeout(self.config.timeout_per_evaluation):
                async for chunk in self.client.stream_completion(messages):
                    if chunk.startswith("<think>"):
                        print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                        continue
                    result_buffer.append(chunk)
                    
            # Parse evaluation result
            result_text = "".join(result_buffer)
            lines = result_text.split("\n")
            
            # Extract score, feedback, and improvements
            score = float([l for l in lines if "Score:" in l][0].split(":")[1].strip())
            
            # Add think process to metadata
            metadata = {"think_process": "Evaluated content against criteria"}
            feedback = [l.strip() for l in lines if "Feedback:" in l]
            improvements = [l.strip() for l in lines if "Improvement:" in l]
            
            return EvaluationResult(
                score=score,
                feedback=feedback,
                improvements=improvements,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"Error during evaluation: {str(e)}")
            raise
            
    async def _improve(self, content: str, evaluation: EvaluationResult, criteria: List[str]) -> str:
        """Improve content based on evaluation."""
        try:
            # Prepare improvement context
            improvements_text = "\n".join(evaluation.improvements)
            feedback_text = "\n".join(evaluation.feedback)
            
            messages = [
                {"role": "system", "content": """Improve this content based on the evaluation feedback
                and suggested improvements while following the original criteria."""},
                {"role": "user", "content": f"""Content to improve:\n{content}
                
                Evaluation Score: {evaluation.score}
                Feedback:\n{feedback_text}
                Suggested Improvements:\n{improvements_text}
                
                Original Criteria:\n{', '.join(criteria)}"""}
            ]
            
            result_buffer = []
            async with asyncio.timeout(self.config.timeout_per_improvement):
                async for chunk in self.client.stream_completion(messages):
                    if chunk.startswith("<think>"):
                        print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                        continue
                    result_buffer.append(chunk)
                    
            return "".join(result_buffer)
            
        except Exception as e:
            print(f"Error during improvement: {str(e)}")
            raise
