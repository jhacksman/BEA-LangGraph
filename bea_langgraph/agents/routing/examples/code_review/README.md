# Code Review Router Example

This example demonstrates a simple routing workflow for code review tasks following Anthropic's pattern for effective agents.

## Overview

The code review router classifies code snippets and directs them to appropriate specialists:
- Security Review
- Performance Analysis
- Style Checking
- Testing Review
- Architecture Review
- General Review

## Implementation

The implementation follows key principles from Anthropic's research:
- Simple keyword-based classification
- Clear separation of concerns
- No complex state management
- Direct routing to specialists

## Usage

```python
from bea_langgraph.agents.routing.examples.code_review.workflow import CodeReviewRouter

# Initialize router
router = CodeReviewRouter()

# Route code for review
code = "def validate_password(password: str):"
specialist = await router.route_review(code)
print(specialist)  # Output: "security"
```

## Testing

Run the tests:
```bash
pytest bea_langgraph/agents/routing/examples/code_review/tests/
```

## Design Decisions

See [DESIGN.md](./DESIGN.md) for detailed design decisions and rationale.
