"""
Think tag handling for venice.ai API responses.

This module provides utilities for processing think tags in streaming responses
from the venice.ai API.
"""

from typing import AsyncGenerator, Optional
import json
import re

class ThinkTagHandler:
    """Handler for processing think tags in API responses."""
    
    def __init__(self):
        self._think_buffer = []
        self._in_think_section = False
        self._think_pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    
    def process_chunk(self, chunk: str) -> Optional[str]:
        """Process a response chunk and handle think tags."""
        try:
            if isinstance(chunk, bytes):
                chunk = chunk.decode('utf-8')
            if chunk.startswith('data: '):
                chunk = chunk.replace('data: ', '')
                if chunk == '[DONE]':
                    return None
                    
            data = json.loads(chunk)
            content = data['choices'][0]['delta'].get('content', '')
            
            # Handle combined think tags in one chunk
            if '<think>' in content and '</think>' in content:
                think_content = content.replace('<think>', '').replace('</think>', '')
                self._think_buffer.append(think_content)
                return None
                
            # Handle split think tags
            if '<think>' in content:
                self._in_think_section = True
                self._think_buffer.append(content.replace('<think>', ''))
                return None
                
            if self._in_think_section:
                if '</think>' in content:
                    self._in_think_section = False
                    self._think_buffer.append(content.replace('</think>', ''))
                    return None
                self._think_buffer.append(content)
                return None
                
            return content if content else None
            
        except json.JSONDecodeError:
            return None
            
    def get_think_content(self) -> str:
        """Get the accumulated think section content."""
        content = ''.join(self._think_buffer)
        self._think_buffer = []
        return content.strip()
