# Tool Best Practices

This guide outlines best practices for working with tools in BEA-LangGraph.

## Tool Design

### 1. Keep Tools Simple and Focused
- Each tool should do one thing well
- Avoid complex state management
- Use clear, descriptive names
- Document parameters thoroughly

### 2. Parameter Design
```python
# Good
calculator_tool = Tool(
    name="calculator",
    description="Performs basic calculations",
    parameters={
        "operation": "string (add, subtract, multiply, divide)",
        "numbers": "list[float]"
    }
)

# Bad - Too complex, mixed responsibilities
complex_tool = Tool(
    name="do_everything",
    description="Does multiple unrelated things",
    parameters={
        "calculation": "dict",
        "text_processing": "dict",
        "file_operations": "dict"
    }
)
```

### 3. Error Handling
- Use specific error types
- Provide clear error messages
- Include recovery suggestions
- Log errors appropriately

```python
# Good
try:
    result = await tool.execute(params)
except ValidationError as e:
    log.error(f"Validation failed: {e}")
    return create_tool_response(
        tool=tool.name,
        parameters=params,
        error=f"Invalid parameters: {str(e)}"
    )
except ToolError as e:
    log.error(f"Tool execution failed: {e}")
    return create_tool_response(
        tool=tool.name,
        parameters=params,
        error=f"Execution failed: {str(e)}"
    )
```

## Message Formatting

### 1. Think Tag Usage
- Use think tags for reasoning steps
- Keep think tag content concise
- Don't include implementation details

```python
# Good
<think>Analyzing input parameters</think>
<think>Validating calculation request</think>
<think>Computing result</think>

# Bad - Too verbose, implementation details
<think>Entering function calculate_result with parameters {}</think>
<think>Checking if numbers list is empty using len() function</think>
```

### 2. Response Formatting
- Use structured formats
- Include relevant metadata
- Keep responses focused

```python
# Good
response = MCPResponse(
    content="The calculation result is 42",
    think_process=["Validating input", "Performing calculation"],
    tool_calls=[
        ToolCall(
            tool="calculator",
            parameters={"operation": "add", "numbers": [20, 22]},
            result="42"
        )
    ]
)

# Bad - Mixed concerns, unstructured
response = "Debug: entering calculation\nValidating...\nResult=42\nExiting..."
```

## Testing

### 1. Test Coverage
- Test normal operation
- Test error cases
- Test edge cases
- Test timeouts

```python
@pytest.mark.asyncio
async def test_calculator_tool():
    """Comprehensive tool testing."""
    # Test normal operation
    result = await calculator.execute({"operation": "add", "numbers": [1, 2]})
    assert result == "3"
    
    # Test error case
    with pytest.raises(ValidationError):
        await calculator.execute({"operation": "invalid"})
    
    # Test edge case
    result = await calculator.execute({"operation": "add", "numbers": []})
    assert result == "0"
```

### 2. Integration Testing
- Test tool chains
- Test error propagation
- Test state management
- Test resource cleanup

## Performance

### 1. Resource Management
- Use async/await properly
- Implement timeouts
- Clean up resources
- Monitor memory usage

### 2. Caching
- Cache expensive operations
- Implement cache invalidation
- Use appropriate cache sizes
- Monitor cache hit rates

## Security

### 1. Input Validation
- Validate all parameters
- Sanitize inputs
- Check permissions
- Rate limit requests

### 2. Error Messages
- Don't expose internals
- Use safe error messages
- Log security events
- Monitor suspicious activity

## Monitoring

### 1. Metrics
- Track execution time
- Monitor error rates
- Count usage patterns
- Alert on anomalies

### 2. Logging
- Use structured logging
- Include context
- Log appropriate levels
- Rotate logs properly
