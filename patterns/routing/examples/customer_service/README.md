# Customer Service Routing Example

This example demonstrates a simple routing workflow that classifies customer service queries and directs them to specialized handlers. Following Anthropic's pattern for effective agents, it implements a straightforward classification system without complex state management.

## Overview

The router classifies incoming customer queries into three main categories:
- Technical Support (product issues, bugs, errors)
- Billing/Refunds (payment issues, refund requests)
- General Inquiries (product information, help)

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

# Define routes for customer service
routes = [
    Route(
        name="technical",
        description="Technical support issues",
        criteria=["error", "bug", "crash", "not working", "broken"],
        handler="technical_support_handler"
    ),
    Route(
        name="billing",
        description="Billing and refund requests",
        criteria=["refund", "charge", "payment", "bill", "subscription"],
        handler="billing_handler"
    ),
    Route(
        name="general",
        description="General product inquiries",
        criteria=["question", "help", "information", "how to"],
        handler="general_inquiry_handler"
    )
]

# Initialize router with routes
router = Router(routes=routes, default_handler="general_inquiry_handler")
```

## Usage Example

```python
async def handle_customer_query(query: str):
    """Handle a customer service query."""
    # Route the query to appropriate handler
    handler_name = await router.route(query)
    
    # Example queries and their routing:
    queries = [
        "My app keeps crashing when I try to login",  # -> technical_support_handler
        "I need a refund for my last payment",        # -> billing_handler
        "How do I use this feature?",                 # -> general_inquiry_handler
        "The system is giving me an error",          # -> technical_support_handler
        "Can you help me understand pricing?",       # -> general_inquiry_handler
    ]
```

## Testing

```python
import pytest

@pytest.mark.asyncio
async def test_customer_service_routing():
    """Test customer service query routing."""
    test_cases = [
        ("My app is crashing", "technical_support_handler"),
        ("I need a refund", "billing_handler"),
        ("How do I use this?", "general_inquiry_handler"),
        ("Payment not working", "billing_handler"),
        ("Random unrelated query", "general_inquiry_handler"),  # Default handler
    ]
    
    for query, expected_handler in test_cases:
        handler = await router.route(query)
        assert handler == expected_handler
```

## Design Decisions

1. Simple Classification
   - Direct mapping of keywords to handlers
   - No complex state management
   - Clear routing logic

2. Default Handler
   - Unclassified queries go to general inquiries
   - Ensures all queries are handled

3. Extensibility
   - Easy to add new routes
   - Simple to update criteria
   - Clear handler interface

## Integration with Model Context Protocol

The router integrates with MCP by:
1. Using standardized input/output formats
2. Supporting tool-based interactions
3. Maintaining clear documentation

## References
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
