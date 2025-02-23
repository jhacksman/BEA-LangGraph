"""
Venice.ai API client implementation.

This module provides a client for interacting with the venice.ai API,
handling think tags and streaming responses.
"""

import asyncio
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
        timeout: float = 120.0
    ) -> AsyncGenerator[str, None]:
        """Stream a chat completion from the API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use for completion
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            timeout: Request timeout in seconds
            
        Yields:
            Generated text chunks with think tags processed
        """
        if not messages:
            raise ValueError("Messages cannot be empty")
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
            
        handler = ThinkTagHandler()
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
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
                        },
                        timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            raise Exception(f"API request failed: {response.status} - {error_text}")
                        
                        async for line in response.content:
                            if not line:
                                continue
                                
                            chunk = line.decode('utf-8').strip()
                            if not chunk or chunk == 'data: [DONE]':
                                continue
                                
                            if not chunk.startswith('data: '):
                                print(f"Unexpected chunk format: {chunk}")
                                continue
                                
                            try:
                                data = json.loads(chunk[6:])  # Skip 'data: ' prefix
                                if not isinstance(data, dict) or 'choices' not in data:
                                    continue
                                    
                                if not data.get('choices') or not isinstance(data['choices'], list):
                                    continue
                                delta = data['choices'][0].get('delta', {})
                                if not isinstance(delta, dict):
                                    continue
                                content = delta.get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError as e:
                                print(f"Failed to parse chunk: {chunk} - {str(e)}")
                            except Exception as e:
                                print(f"Error processing chunk: {str(e)}")
                                continue
                        return
                        
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise Exception(f"API request failed after {max_retries} attempts: {str(e)}")
                print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
