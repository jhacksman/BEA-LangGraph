# Basic Workflow Pattern

## Overview
Implementation of document processing workflow following Anthropic's pattern for basic workflows. This pattern provides a structured approach to document generation, review, and revision using LLM-based agents.

## Components

### Document Generation
- Creates initial document based on provided criteria
- Handles streaming responses with think tag processing
- Implements timeout and error handling

### Document Review
- Analyzes document against specified criteria
- Provides structured feedback
- Supports streaming review process

### Document Revision
- Improves document based on review feedback
- Maintains document history
- Handles multi-step revision process

## Implementation

### Workflow Configuration
```python
from .models import WorkflowConfig
from .api.client import VeniceClient

config = WorkflowConfig(
    criteria=["clarity", "completeness", "accuracy"],
    max_retries=3
)
client = VeniceClient(api_key="your_api_key")
workflow = DocumentWorkflow(config, client)
```

### Running the Workflow
```python
result = await workflow.run({
    "document": DocumentState(content=""),
    "config": config
})
```

### State Management
The workflow maintains document state through the `DocumentState` class:
- Content tracking
- Review feedback history
- Revision history

## Usage Examples

### Basic Document Generation
```python
# Initialize workflow
workflow = DocumentWorkflow(config, client)

# Generate document
result = await workflow.run()
print(result["document"].content)
```

### Document Review and Revision
```python
# Run workflow with review and revision
result = await workflow.run()
doc_state = result["document"]

# Access review feedback
print(doc_state.review_feedback)

# Access revision history
print(doc_state.revision_history)
```

## Testing

### Unit Tests
- Test document generation
- Test review process
- Test revision handling
- Test error cases

### Integration Tests
```python
async def test_workflow_integration():
    """Test complete workflow execution."""
    workflow = DocumentWorkflow(config, client)
    result = await workflow.run()
    
    assert result["document"].content
    assert len(result["document"].review_feedback) > 0
    assert len(result["document"].revision_history) > 0
```

## Error Handling
- Timeout handling for each step
- Graceful fallback for partial content
- Clear error reporting
- Retry mechanism for failed operations

## References
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
