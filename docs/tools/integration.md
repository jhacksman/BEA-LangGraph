# Tool Integration Guide

This guide explains how to integrate new tools and customize message formats in BEA-LangGraph.

## Adding New Tools

1. Define Tool Specification
```python
from bea_langgraph.common.mcp import Tool

new_tool = Tool(
    name="my_tool",
    description="Tool description",
    parameters={
        "param1": "string",
        "param2": "int"
    }
)
```

2. Implement Tool Handler
```python
async def handle_my_tool(parameters: Dict[str, Any]) -> str:
    """Handle tool execution."""
    try:
        result = # Tool implementation
        return result
    except Exception as e:
        raise Exception(f"Tool execution failed: {str(e)}")
```

3. Register Tool
```python
tools = {
    "my_tool": handle_my_tool
}
```

## Message Format Customization

1. Extend Base Models
```python
from bea_langgraph.common.mcp import MCPMessage

class CustomMessage(MCPMessage):
    """Custom message format."""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=0)
```

2. Custom Think Tag Processing
```python
def custom_think_processor(response: str) -> List[str]:
    """Custom think tag processor."""
    # Implementation
    return think_tags
```

## Testing Tools

1. Unit Tests
```python
import pytest
from bea_langgraph.common.mcp import create_tool_response

@pytest.mark.asyncio
async def test_my_tool():
    """Test tool functionality."""
    result = create_tool_response(
        tool="my_tool",
        parameters={"param1": "test", "param2": 42}
    )
    assert result.error is None
    assert result.result == "expected output"
```

2. Integration Tests
```python
@pytest.mark.asyncio
async def test_tool_workflow():
    """Test tool in workflow."""
    workflow = MyWorkflow(tools=[my_tool])
    result = await workflow.run()
    assert result.tool_calls
```

## Error Handling

1. Tool-specific Errors
```python
class ToolError(Exception):
    """Base class for tool errors."""
    pass

class ValidationError(ToolError):
    """Validation error in tool parameters."""
    pass
```

2. Error Recovery
```python
try:
    result = await tool.execute(parameters)
except ToolError as e:
    # Handle tool-specific error
    error_response = create_tool_response(
        tool=tool.name,
        parameters=parameters,
        error=str(e)
    )
except Exception as e:
    # Handle unexpected errors
    error_response = create_tool_response(
        tool=tool.name,
        parameters=parameters,
        error=f"Unexpected error: {str(e)}"
    )
```

## Monitoring and Logging

1. Tool Metrics
```python
async def execute_tool(tool: Tool, parameters: Dict[str, Any]) -> ToolCall:
    """Execute tool with monitoring."""
    start_time = time.time()
    try:
        result = await tool.execute(parameters)
        duration = time.time() - start_time
        log_tool_metrics(tool.name, duration, success=True)
        return create_tool_response(
            tool=tool.name,
            parameters=parameters,
            result=result
        )
    except Exception as e:
        duration = time.time() - start_time
        log_tool_metrics(tool.name, duration, success=False)
        raise
```

2. Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('bea_langgraph.tools')
```
