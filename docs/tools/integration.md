# Tool Integration Guide

This guide explains how to integrate tools and patterns in BEA-LangGraph following Anthropic's research on building effective agents and the Model Context Protocol.

## Core Principles

1. **Simplicity**
   - Keep tools focused and minimal
   - Clear interfaces
   - Direct implementations

2. **Composability**
   - Easy pattern integration
   - Standard formats
   - Modular design

3. **Reliability**
   - Consistent error handling
   - Clear documentation
   - Thorough testing

## Tool Integration

1. **Define Tool with Examples**
```python
from bea_langgraph.common.mcp import Tool

calculator = Tool(
    name="calculator",
    description="Performs basic calculations",
    parameters={
        "operation": "string",
        "numbers": "list[float]"
    },
    examples=[{
        "input": {
            "operation": "add",
            "numbers": [1, 2]
        },
        "output": "3"
    }]
)
```

2. **Implement Handler Following MCP**
```python
from bea_langgraph.common.mcp import create_tool_response

async def handle_calculator(parameters: Dict[str, Any]) -> str:
    """Handle calculation following MCP specification."""
    try:
        operation = parameters["operation"]
        numbers = parameters["numbers"]
        
        if operation == "add":
            result = sum(numbers)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
            
        return create_tool_response(
            tool="calculator",
            parameters=parameters,
            result=str(result)
        )
    except Exception as e:
        return create_tool_response(
            tool="calculator",
            parameters=parameters,
            error=str(e)
        )
```

3. **Document Tool**
```python
from bea_langgraph.common.mcp import document_tool

# Generate standardized documentation
docs = document_tool(calculator)
print(docs)  # Outputs formatted documentation
```

## Pattern Integration

1. **Basic Workflow Pattern**
```python
from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow

workflow = DocumentWorkflow(
    tools=[calculator],
    config={"think_tags": True}
)
result = await workflow.run(input_data)
```

2. **Routing Pattern**
```python
from bea_langgraph.agents.routing.router import Router

router = Router(routes={
    "math": ["calculate", "sum", "add"],
    "text": ["format", "edit", "write"]
})
```

3. **Parallelization Pattern**
```python
from bea_langgraph.agents.parallelization.workflow import ParallelWorkflow

workflow = ParallelWorkflow(tools=[calculator])
results = await workflow.process_tasks(tasks)
```

## Testing and Validation

1. **Unit Tests**
```python
import pytest
from bea_langgraph.common.mcp import Tool, create_tool_response

@pytest.mark.asyncio
async def test_calculator():
    """Test calculator tool following MCP."""
    # Test successful case
    result = await handle_calculator({
        "operation": "add",
        "numbers": [1, 2]
    })
    assert result.result == "3"
    assert not result.error
    
    # Test error case
    result = await handle_calculator({
        "operation": "unknown",
        "numbers": [1]
    })
    assert result.error
    assert "Unsupported operation" in result.error
```

2. **Pattern Integration Tests**
```python
@pytest.mark.asyncio
async def test_workflow_integration():
    """Test tool in workflow patterns."""
    # Test basic workflow
    workflow = DocumentWorkflow(tools=[calculator])
    result = await workflow.run({"content": "Calculate 1 + 2"})
    assert "3" in result["document"].content
    
    # Test routing
    router = Router(routes={"math": ["calculate", "add"]})
    route = await router.route("Calculate 1 + 2")
    assert route == "math"
```

## Best Practices

1. **Tool Design**
   - Follow single responsibility principle
   - Provide clear examples
   - Document thoroughly
   - Handle errors gracefully

2. **Pattern Integration**
   - Use appropriate patterns
   - Keep implementations simple
   - Test interactions
   - Document combinations

3. **Error Management**
   - Use MCP error format
   - Provide clear messages
   - Handle edge cases
   - Log appropriately

See [best_practices.md](best_practices.md) for more details.
