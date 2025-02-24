"""API response handlers for routing agent."""

from typing import Dict, Any, List, Optional
from ...basic_workflow.api.handlers import ResponseHandler

class RoutingResponseHandler(ResponseHandler):
    """Handler for routing-specific API responses."""
    
    def __init__(self):
        """Initialize the handler."""
        super().__init__()
        self._current_route: Optional[str] = None
        self._confidence: float = 0.0
        self._reasoning: List[str] = []
        
    @property
    def route(self) -> Optional[str]:
        """Get the selected route."""
        return self._current_route
        
    @property
    def confidence(self) -> float:
        """Get the confidence score."""
        return self._confidence
        
    @property
    def reasoning(self) -> List[str]:
        """Get the reasoning steps."""
        return self._reasoning
        
    def process_chunk(self, chunk: str) -> None:
        """Process a response chunk."""
        if chunk.startswith("<think>"):
            # Extract reasoning from think tags
            reasoning = chunk[7:-8].strip()  # Remove <think> tags
            self._reasoning.append(reasoning)
            return
            
        # Look for route selection indicators
        lower_chunk = chunk.lower()
        route_indicators = [
            "selected route:", "chosen route:",
            "recommend route:", "best route:",
            "route selection:"
        ]
        
        for indicator in route_indicators:
            if indicator in lower_chunk:
                # Extract route name after indicator
                start_idx = lower_chunk.index(indicator) + len(indicator)
                end_idx = chunk.find("\n", start_idx)
                if end_idx == -1:
                    end_idx = len(chunk)
                self._current_route = chunk[start_idx:end_idx].strip()
                
                # Update confidence based on certainty indicators
                self._update_confidence(chunk)
                break
                
    def _update_confidence(self, chunk: str) -> None:
        """Update confidence score based on response content."""
        lower_chunk = chunk.lower()
        
        # Confidence boosters
        certainty_indicators = [
            "definitely", "certainly", "clearly",
            "perfect match", "strongly recommend",
            "obvious choice", "exact match"
        ]
        
        # Confidence reducers
        uncertainty_indicators = [
            "might be", "possibly", "perhaps",
            "not sure", "could be", "uncertain",
            "alternatively"
        ]
        
        base_confidence = 0.7  # Start with reasonable confidence
        
        for indicator in certainty_indicators:
            if indicator in lower_chunk:
                base_confidence += 0.1
                
        for indicator in uncertainty_indicators:
            if indicator in lower_chunk:
                base_confidence -= 0.1
                
        self._confidence = min(max(base_confidence, 0.0), 1.0)
