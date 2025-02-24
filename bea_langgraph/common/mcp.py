"""
Model Context Protocol integration.

This module implements standardized message formats and tool integration
following the Model Context Protocol specification.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Tool(BaseModel):
    """Model for tool specification."""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class ToolCall(BaseModel):
    """Model for tool call results."""
    tool: str
    parameters: Dict[str, Any]
    result: Optional[str] = None
    error: Optional[str] = None
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class MCPMessage(BaseModel):
    """Model for MCP-compliant messages."""
    role: str
    content: str
    think_tags: Optional[List[str]] = None
    tools: Optional[List[Tool]] = None
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

class MCPResponse(BaseModel):
    """Model for MCP-compliant responses."""
    content: str
    think_process: List[str] = Field(default_factory=list)
    tool_calls: List[ToolCall] = Field(default_factory=list)
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

def process_think_tags(response: str) -> MCPResponse:
    """Process response text and extract think tags."""
    think_process = []
    content_parts = []
    
    # Split response into parts
    parts = response.split("<think>")
    for part in parts:
        if "</think>" in part:
            think_tag, content = part.split("</think>", 1)
            think_process.append(think_tag.strip())
            content_parts.append(content)
        else:
            content_parts.append(part)
    
    return MCPResponse(
        content="".join(content_parts).strip(),
        think_process=think_process
    )

def create_tool_response(tool: str, parameters: Dict[str, Any], result: Optional[str] = None, error: Optional[str] = None) -> ToolCall:
    """Create a standardized tool call response."""
    return ToolCall(
        tool=tool,
        parameters=parameters,
        result=result,
        error=error
    )
