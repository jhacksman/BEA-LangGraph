# Document Generation Example

This example demonstrates a simple document generation workflow following Anthropic's pattern for basic workflows. It implements a straightforward generation process that creates documents based on specified criteria.

## Overview

The workflow handles document generation with:
- Initial content creation based on criteria
- Streaming response processing
- Think tag handling
- Error management

## Implementation

### Basic Generation
```python
from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow
from bea_langgraph.agents.basic_workflow.models import WorkflowConfig
from bea_langgraph.agents.basic_workflow.api.client import VeniceClient

# Initialize workflow
config = WorkflowConfig(
    criteria=["clear structure", "concise content", "technical accuracy"]
)
client = VeniceClient(api_key="your_api_key")
workflow = DocumentWorkflow(config, client)

# Generate document
result = await workflow.run()
print(result["document"].content)
```

### Advanced Usage
```python
# Custom generation criteria
config = WorkflowConfig(
    criteria=[
        "include executive summary",
        "technical details in appendix",
        "clear recommendations"
    ],
    max_retries=3
)

# Run with custom state
result = await workflow.run({
    "document": DocumentState(
        content="Initial draft content..."
    ),
    "config": config
})
```

## Testing

### Unit Tests
```python
async def test_document_generation():
    """Test basic document generation."""
    workflow = DocumentWorkflow(config, client)
    result = await workflow.run()
    
    assert result["document"].content
    assert len(result["document"].content) > 200
```

### Integration Tests
```python
async def test_generation_with_criteria():
    """Test generation with specific criteria."""
    config = WorkflowConfig(
        criteria=["technical accuracy", "clear structure"]
    )
    workflow = DocumentWorkflow(config, client)
    result = await workflow.run()
    
    assert any(c in result["document"].content.lower() 
              for c in ["technical", "structure"])
```

## Error Handling
- Timeout handling for long generations
- Partial content recovery
- Retry mechanism for failed attempts
- Clear error reporting

## References
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
