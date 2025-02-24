"""Router implementation for routing agent pattern."""

import asyncio
from typing import Dict, Any, List, Tuple, cast
from .models import RouterConfig, RoutingState, Route
from ..basic_workflow.api.client import VeniceClient

class Router:
    """Implementation of routing agent."""
    
    def __init__(self, config: RouterConfig, client: VeniceClient):
        """Initialize router with configuration and API client."""
        self.config = config
        self.client = client
        
    async def route(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Route input to appropriate handler based on content."""
        routing_state = cast(RoutingState, state.get("routing"))
        if not routing_state:
            raise ValueError("No routing state provided")
            
        try:
            route, confidence = await self._select_route(routing_state.input)
            routing_state.set_route(route.name, confidence)
            
            if confidence < self.config.confidence_threshold:
                if routing_state.attempts >= self.config.max_retries:
                    routing_state.set_route(self.config.default_handler, 1.0)
                else:
                    # Try again with more context
                    return await self.route(state)
                    
            return {"routing": routing_state}
        except Exception as e:
            raise Exception(f"Routing failed: {str(e)}")
            
    async def _select_route(self, input_text: str) -> Tuple[Route, float]:
        """Select appropriate route based on input text."""
        messages = [
            {"role": "system", "content": "You are a routing assistant. Select the most appropriate route based on the input."},
            {"role": "user", "content": self._create_routing_prompt(input_text)}
        ]
        
        try:
            route_selection = ""
            confidence = 0.0
            
            async with asyncio.timeout(30):
                async for chunk in self.client.stream_completion(messages, timeout=30.0):
                    if chunk.startswith("<think>"):
                        continue
                    route_selection += chunk
                    
            # Parse route selection and confidence
            for route in self.config.routes:
                if route.name.lower() in route_selection.lower():
                    confidence = self._calculate_confidence(route_selection)
                    return route, confidence
                    
            raise ValueError(f"No matching route found for input: {input_text}")
        except Exception as e:
            raise Exception(f"Route selection failed: {str(e)}")
            
    def _create_routing_prompt(self, input_text: str) -> str:
        """Create prompt for route selection."""
        routes_desc = "\n".join([
            f"Route: {r.name}\nDescription: {r.description}\nCriteria: {', '.join(r.criteria)}"
            for r in self.config.routes
        ])
        
        return f"""Please analyze this input and select the most appropriate route:

Input:
{input_text}

Available Routes:
{routes_desc}

Select the most appropriate route name and explain your reasoning."""
            
    def _calculate_confidence(self, route_selection: str) -> float:
        """Calculate confidence score from route selection response."""
        # Simple heuristic based on response length and certainty indicators
        confidence = 0.5  # Base confidence
        
        certainty_indicators = [
            "definitely", "certainly", "clearly", "perfect match",
            "strongly", "obvious", "exact", "precisely"
        ]
        
        uncertainty_indicators = [
            "might", "maybe", "possibly", "perhaps", "unclear",
            "not sure", "could be", "uncertain"
        ]
        
        for indicator in certainty_indicators:
            if indicator in route_selection.lower():
                confidence += 0.1
                
        for indicator in uncertainty_indicators:
            if indicator in route_selection.lower():
                confidence -= 0.1
                
        return min(max(confidence, 0.0), 1.0)
