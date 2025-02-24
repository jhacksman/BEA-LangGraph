# Tool Usage Guide

This guide explains how to use tools with the BEA-LangGraph library following the Model Context Protocol (MCP) and Anthropic's research on building effective agents.

## Overview

Tools in BEA-LangGraph are implemented following the MCP specification and Anthropic's guidance:

1. **Simplicity**
   - Clear, focused tools
   - Direct interfaces
   - Minimal state management

2. **Standardization**
   - MCP message formats
   - Think tag processing
   - Consistent error handling

3. **Composability**
   - Easy integration with patterns
   - Modular design
   - Clear interfaces

## Basic Usage

Following Anthropic's guidance for clear, focused tools:

```python
from bea_langgraph.common.mcp import MCPMessage, Tool

# Define a tool with examples
tool = Tool(
    name="calculator",
    description="Performs basic calculations",
    parameters={
        "operation": "string",
        "numbers": "list[float]"
    },
    examples=[{
        "input": {
            "operation": "add",
            "numbers": [2, 2]
        },
        "output": "4"
    }]
)

# Create a message with tool
message = MCPMessage(
    role="user",
    content="Calculate 2 + 2",
    tools=[tool]
)

# Document the tool
from bea_langgraph.common.mcp import document_tool
docs = document_tool(tool)  # Get standardized documentation
```

### Tool Design Principles

1. **Single Responsibility**
   - Each tool should do one thing well
   - Clear input/output interface
   - Focused functionality

2. **Clear Documentation**
   - Descriptive names
   - Example usage
   - Parameter descriptions

3. **Error Handling**
   - Predictable errors
   - Clear messages
   - Recovery guidance

## Think Tag Processing

```python
from bea_langgraph.common.mcp import process_think_tags

response = """<think>Analyzing calculation request</think>
The result is 4
<think>Verifying result</think>
Confirmed: 2 + 2 = 4"""

mcp_response = process_think_tags(response)
print(mcp_response.think_process)  # ['Analyzing calculation request', 'Verifying result']
print(mcp_response.content)  # 'The result is 4\nConfirmed: 2 + 2 = 4'
```

## Tool Calls

```python
from bea_langgraph.common.mcp import create_tool_response

result = create_tool_response(
    tool="calculator",
    parameters={"operation": "add", "numbers": [2, 2]},
    result="4"
)
```

## Error Handling

```python
# Handle tool errors
error_result = create_tool_response(
    tool="calculator",
    parameters={"operation": "divide", "numbers": [1, 0]},
    error="Division by zero"
)
```

## Best Practices

See [best_practices.md](best_practices.md) for detailed guidelines on:
- Tool design
- Error handling
- Message formatting
- Think tag usage

## Integration

See [integration.md](integration.md) for details on:
- Adding new tools
- Customizing message formats
- Extending functionality
- Testing tools
