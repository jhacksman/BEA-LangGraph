# Model Selection Routing Example

This example demonstrates a simple routing workflow that directs queries to different models based on their complexity. Following Anthropic's pattern for effective agents, it implements straightforward classification without complex state management.

## Overview

The router classifies incoming queries into two main categories:
- Simple/Common Queries (routed to smaller, faster models)
- Complex/Unusual Queries (routed to more capable models)

## Implementation

```python
from typing import List
from pydantic import BaseModel

class Route(BaseModel):
    """Defines a route with its handler and criteria."""
    name: str
    description: str
    criteria: List[str]
    handler: str

# Define routes for model selection
routes = [
    Route(
        name="simple",
        description="Simple or common queries",
        criteria=[
            "basic", "common", "straightforward",
            "what is", "how to", "where can I",
            "help me find", "explain"
        ],
        handler="small_model_handler"  # e.g., GPT-3.5
    ),
    Route(
        name="complex",
        description="Complex or unusual queries",
        criteria=[
            "analyze", "compare", "evaluate",
            "synthesize", "complex", "unusual",
            "edge case", "technical", "advanced"
        ],
        handler="large_model_handler"  # e.g., GPT-4
    )
]

# Initialize router with routes
router = Router(routes=routes, default_handler="large_model_handler")
```

## Usage Example

```python
async def route_query(query: str):
    """Route a query to the appropriate model."""
    # Route the query to appropriate handler
    handler_name = await router.route(query)
    
    # Example queries and their routing:
    queries = [
        "What is the capital of France?",           # -> small_model_handler
        "How do I reset my password?",              # -> small_model_handler
        "Analyze the implications of quantum...",    # -> large_model_handler
        "Compare these complex architectural...",    # -> large_model_handler
        "Help me find the nearest store",           # -> small_model_handler
    ]
```

## Testing

```python
import pytest

@pytest.mark.asyncio
async def test_model_selection_routing():
    """Test query routing to appropriate models."""
    test_cases = [
        ("What is the weather today?", "small_model_handler"),
        ("Analyze the economic impact...", "large_model_handler"),
        ("How do I make coffee?", "small_model_handler"),
        ("Compare quantum computing approaches", "large_model_handler"),
        ("Unknown complex query", "large_model_handler"),  # Default to capable model
    ]
    
    for query, expected_handler in test_cases:
        handler = await router.route(query)
        assert handler == expected_handler
```

## Design Decisions

1. Simple Classification
   - Direct mapping of complexity indicators
   - No complex state management
   - Clear routing logic

2. Default Handler
   - Unclassified queries go to large model
   - Better to use more capable model when uncertain
   - Ensures all queries get appropriate handling

3. Extensibility
   - Easy to add new model handlers
   - Simple to update criteria
   - Clear handler interface

## Integration with Model Context Protocol

The router integrates with MCP by:
1. Using standardized input/output formats
2. Supporting tool-based interactions
3. Maintaining clear documentation

## Cost and Performance Considerations

1. Optimization
   - Route common queries to smaller, faster models
   - Use more capable models only when needed
   - Balance cost vs. capability

2. Monitoring
   - Track routing accuracy
   - Monitor model performance
   - Adjust criteria based on results

## References
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
