"""Tests for Model Context Protocol integration."""

import pytest
from bea_langgraph.common.mcp import (
    Tool, ToolCall, MCPMessage, MCPResponse,
    process_think_tags, create_tool_response, document_tool
)

def test_tool_model():
    """Test Tool model validation."""
    tool = Tool(
        name="test_tool",
        description="Test tool",
        parameters={"param1": "string"},
        examples=[{
            "input": {"param1": "test"},
            "output": "success"
        }]
    )
    assert tool.name == "test_tool"
    assert tool.parameters == {"param1": "string"}
    assert len(tool.examples) == 1

def test_tool_call_model():
    """Test ToolCall model validation."""
    call = ToolCall(
        tool="test_tool",
        parameters={"param1": "value"},
        result="success"
    )
    assert call.tool == "test_tool"
    assert call.result == "success"
    assert call.error is None

def test_mcp_message():
    """Test MCPMessage model validation."""
    tool = Tool(
        name="test_tool",
        description="Test tool",
        parameters={}
    )
    message = MCPMessage(
        role="user",
        content="Test content",
        tools=[tool]
    )
    assert message.role == "user"
    assert len(message.tools) == 1
    assert message.think_tags is None

def test_mcp_response():
    """Test MCPResponse model validation."""
    tool_call = ToolCall(
        tool="test_tool",
        parameters={},
        result="success"
    )
    response = MCPResponse(
        content="Test response",
        think_process=["Thinking step 1"],
        tool_calls=[tool_call]
    )
    assert response.content == "Test response"
    assert len(response.think_process) == 1
    assert len(response.tool_calls) == 1

def test_process_think_tags():
    """Test think tag processing."""
    response_text = """<think>Step 1</think>
    Processing...
    <think>Step 2</think>
    Done!"""
    
    result = process_think_tags(response_text)
    assert len(result.think_process) == 2
    assert result.think_process == ["Step 1", "Step 2"]
    assert "Processing..." in result.content
    assert "Done!" in result.content
    assert "<think>" not in result.content

def test_create_tool_response():
    """Test tool response creation."""
    # Success case
    success = create_tool_response(
        tool="test_tool",
        parameters={"param": "value"},
        result="success"
    )
    assert success.tool == "test_tool"
    assert success.result == "success"
    assert success.error is None
    
    # Error case
    error = create_tool_response(
        tool="test_tool",
        parameters={"param": "value"},
        error="Failed"
    )
    assert error.tool == "test_tool"
    assert error.result is None
    assert error.error == "Failed"

def test_think_tag_edge_cases():
    """Test think tag processing edge cases."""
    # Empty response
    empty = process_think_tags("")
    assert empty.content == ""
    assert not empty.think_process
    
    # No think tags
    no_tags = process_think_tags("Just content")
    assert no_tags.content == "Just content"
    assert not no_tags.think_process
    
    # Malformed tags
    malformed = process_think_tags("<think>Incomplete tag\nContent")
    assert "Content" in malformed.content
    assert not malformed.think_process

def test_tool_validation():
    """Test tool model validation."""
    with pytest.raises(ValueError):
        Tool(name="", description="Invalid tool", parameters={})  # Empty name
    
    with pytest.raises(ValueError):
        Tool(name="test", description="Test", parameters={}, examples=[{}])  # Invalid example
        
    with pytest.raises(ValueError):
        ToolCall(tool="test", parameters=None)  # None parameters

def test_tool_documentation():
    """Test tool documentation generation."""
    # Test basic tool documentation
    tool = Tool(
        name="calculator",
        description="Performs basic calculations",
        parameters={
            "operation": "string",
            "numbers": "list[float]"
        }
    )
    doc = document_tool(tool)
    assert "Tool: calculator" in doc
    assert "Performs basic calculations" in doc
    assert "operation: string" in doc
    assert "numbers: list[float]" in doc
    
    # Test tool documentation with examples
    tool_with_examples = Tool(
        name="calculator",
        description="Performs basic calculations",
        parameters={
            "operation": "string",
            "numbers": "list[float]"
        },
        examples=[
            {
                "input": {
                    "operation": "add",
                    "numbers": [1.0, 2.0]
                },
                "output": "3.0"
            }
        ]
    )
    doc = document_tool(tool_with_examples)
    assert "Examples:" in doc
    assert "Input:" in doc
    assert "operation: add" in doc
    assert "Output:" in doc
    assert "3.0" in doc

def test_tool_documentation_edge_cases():
    """Test tool documentation edge cases."""
    # Empty parameters
    tool = Tool(
        name="test",
        description="Test tool",
        parameters={}
    )
    doc = document_tool(tool)
    assert "Parameters:\n  None" in doc
    
    # No examples
    assert "Examples:" not in doc
    
    # Empty examples list
    tool = Tool(
        name="test",
        description="Test tool",
        parameters={},
        examples=[]
    )
    doc = document_tool(tool)
    assert "Examples:" not in doc
