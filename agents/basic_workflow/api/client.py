"""
Venice.ai API client implementation.

This module provides a client for interacting with the venice.ai API,
handling think tags and streaming responses.
"""

import aiohttp
from typing import AsyncGenerator, List, Dict, Any
import json
from .handlers import ThinkTagHandler

class VeniceClient:
    """Client for interacting with the venice.ai API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.venice.ai/api/v1"):
        """Initialize the Venice API client.
        
        Args:
            api_key: Venice API key
            base_url: Base URL for the Venice API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def stream_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-r1-671b",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AsyncGenerator[str, None]:
        """Stream a chat completion from the API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use for completion
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Yields:
            Generated text chunks with think tags removed
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True
                }
            ) as response:
                handler = ThinkTagHandler()
                
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                
                async for line in response.content:
                    if line:
                        chunk = line.decode('utf-8').strip()
                        if chunk and chunk != "data: [DONE]":
                            processed = handler.process_chunk(chunk)
                            if processed:
                                yield processed
                            elif not handler._in_think_section and handler.get_think_content():
                                yield f"__THINK__: {handler.get_think_content()}"
