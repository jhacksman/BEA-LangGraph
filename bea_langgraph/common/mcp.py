"""
Model Context Protocol integration.

This module implements standardized message formats and tool integration
following the Model Context Protocol specification.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Tool(BaseModel):
    """Model for tool specification."""
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    examples: Optional[List[Dict[str, Any]]] = Field(default=None)
    
    @property
    def has_examples(self) -> bool:
        """Check if tool has valid examples."""
        return bool(self.examples and all(
            isinstance(ex, dict) and 'input' in ex and 'output' in ex
            for ex in self.examples
        ))
    
    def __init__(self, **data):
        """Initialize with validation."""
        super().__init__(**data)
        if not self.name:
            raise ValueError("Tool name cannot be empty")
        if not self.description:
            raise ValueError("Tool description cannot be empty")
        if self.examples and not self.has_examples:
            raise ValueError("Invalid tool examples format")
    
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

def document_tool(tool: Tool) -> str:
    """Generate standardized tool documentation following MCP specification.
    
    Args:
        tool: Tool instance to document
        
    Returns:
        Formatted documentation string
    """
    doc = f"""Tool: {tool.name}
Description: {tool.description}

Parameters:
{_format_parameters(tool.parameters)}"""

    if tool.examples:
        doc += "\n\nExamples:\n"
        for i, example in enumerate(tool.examples, 1):
            doc += f"\n{i}. Input:\n"
            doc += _format_parameters(example.get("input", {}))
            doc += "\n   Output:\n"
            doc += f"   {example.get('output', '')}\n"
    
    return doc

def _format_parameters(params: Dict[str, Any]) -> str:
    """Format parameters dictionary into readable string.
    
    Args:
        params: Parameters dictionary
        
    Returns:
        Formatted parameter string
    """
    if not params:
        return "  None"
    return "\n".join(f"  - {name}: {type_}" for name, type_ in params.items())
