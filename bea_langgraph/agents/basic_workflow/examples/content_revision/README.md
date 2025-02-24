# Content Revision Example

This example demonstrates a content revision workflow following Anthropic's pattern for basic workflows. It implements a straightforward revision process that improves content based on review feedback.

## Overview

The workflow handles content revision with:
- Review feedback processing
- Content improvement based on feedback
- Version history tracking
- Quality validation

## Implementation

### Basic Revision
```python
from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow
from bea_langgraph.agents.basic_workflow.models import WorkflowConfig, DocumentState
from bea_langgraph.agents.basic_workflow.api.client import VeniceClient

# Initialize workflow
config = WorkflowConfig(
    criteria=["clarity", "accuracy", "completeness"]
)
client = VeniceClient(api_key="your_api_key")
workflow = DocumentWorkflow(config, client)

# Run revision workflow
initial_state = {
    "document": DocumentState(
        content="Initial content to revise..."
    ),
    "config": config
}
result = await workflow.run(initial_state)
print(result["document"].revision_history[-1])
```

### Advanced Usage
```python
# Custom revision criteria
config = WorkflowConfig(
    criteria=[
        "technical accuracy",
        "consistent terminology",
        "proper citations"
    ],
    max_retries=3
)

# Run with review feedback
doc_state = DocumentState(
    content="Content to revise...",
    review_feedback=["Improve technical accuracy", "Add citations"]
)
result = await workflow.run({
    "document": doc_state,
    "config": config
})
```

## Testing

### Unit Tests
```python
async def test_content_revision():
    """Test basic content revision."""
    workflow = DocumentWorkflow(config, client)
    doc_state = DocumentState(
        content="Test content",
        review_feedback=["Add more detail"]
    )
    result = await workflow.run({"document": doc_state})
    
    assert result["document"].revision_history
    assert len(result["document"].revision_history) > 0
```

### Integration Tests
```python
async def test_revision_with_feedback():
    """Test revision with specific feedback."""
    doc_state = DocumentState(
        content="Initial content",
        review_feedback=["Improve clarity"]
    )
    result = await workflow.run({"document": doc_state})
    
    assert len(result["document"].revision_history) > 0
    assert result["document"].content != doc_state.content
```

## Error Handling
- Timeout handling for long revisions
- Version history preservation
- Retry mechanism for failed attempts
- Clear error reporting

## References
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
