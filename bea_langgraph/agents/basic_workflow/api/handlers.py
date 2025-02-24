"""
Think tag handling for venice.ai API responses.

This module provides utilities for processing think tags in streaming responses
from the venice.ai API.
"""

from typing import AsyncGenerator, Optional, List
import json
import re

class ResponseHandler:
    """Base class for API response handlers."""
    
    def __init__(self):
        """Initialize the handler."""
        self._buffer = []
        
    def process_chunk(self, chunk: str) -> Optional[str]:
        """Process a response chunk."""
        try:
            content = chunk.strip()
            if not content:
                return None
            return content
        except Exception as e:
            print(f"Error processing chunk: {str(e)}")
            return None

class ThinkTagHandler(ResponseHandler):
    """Handler for processing think tags in API responses."""
    
    def __init__(self):
        self._think_buffer = []
        self._in_think_section = False
        self._think_pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    
    def process_chunk(self, chunk: str) -> Optional[str]:
        """Process a response chunk and handle think tags."""
        try:
            content = chunk.strip()
            if not content:
                return None
                
            # Handle think tags
            if '<think>' in content:
                self._in_think_section = True
                content = content.replace('<think>', '')
            
            if self._in_think_section:
                if '</think>' in content:
                    self._in_think_section = False
                    content = content.replace('</think>', '')
                    self._think_buffer.append(content)
                    think_content = ''.join(self._think_buffer)
                    self._think_buffer = []
                    if think_content.strip():
                        return f"__THINK__: {think_content.strip()}"
                    return None
                self._think_buffer.append(content)
                return None
            
            return content if content.strip() else None
            
        except Exception as e:
            print(f"Error processing chunk: {str(e)}")
            return None
            
        except json.JSONDecodeError:
            return None
            
    def get_think_content(self) -> str:
        """Get the accumulated think section content."""
        content = ''.join(self._think_buffer)
        self._think_buffer = []
        return content.strip()
