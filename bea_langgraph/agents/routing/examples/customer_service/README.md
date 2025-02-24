# Customer Service Router Example

This example demonstrates a simple routing workflow for customer service queries following Anthropic's pattern for effective agents.

## Overview

The customer service router classifies incoming queries and directs them to appropriate departments:
- Technical Support
- Billing
- Account Management
- Product Help
- General Support

## Implementation

The implementation follows key principles from Anthropic's research:
- Simple classification based on keywords
- Clear separation of concerns
- No complex state management
- Direct routing to specialized handlers

## Usage

```python
from bea_langgraph.agents.routing.examples.customer_service.workflow import CustomerServiceRouter

# Initialize router
router = CustomerServiceRouter()

# Route a query
department = await router.route_query("I need help with my payment")
print(department)  # Output: "billing"
```

## Testing

Run the tests:
```bash
pytest bea_langgraph/agents/routing/examples/customer_service/tests/
```

## Design Decisions

See [DESIGN.md](./DESIGN.md) for detailed design decisions and rationale.
