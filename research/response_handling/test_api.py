"""Test script to verify API response handling and think tag processing."""

import os
import asyncio
import aiohttp
import json
from typing import Dict, Any

async def test_api_response():
    """Test Venice.ai API response handling with think tag verification."""
    print("\n=== Testing API Response Handling ===\n")
    
    api_key = os.getenv("VENICE_API_KEY")
    if not api_key:
        raise ValueError("VENICE_API_KEY environment variable not set")
    base_url = os.getenv("VENICE_API_URL", "https://api.venice.ai/api/v1")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Keep responses under 100 words."},
        {"role": "user", "content": "Write a very short story about a cat."}
    ]
    
    try:
        print("1. Testing API connection...")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek-r1-671b",
                    "messages": messages,
                    "stream": True
                },
                timeout=30
            ) as response:
                print(f"Response status: {response.status}")
                print(f"Response headers: {dict(response.headers)}\n")
                
                print("2. Processing streaming response...")
                in_think_tag = False
                think_content = []
                main_content = []
                
                async for line in response.content:
                    if not line:
                        continue
                        
                    chunk = line.decode('utf-8').strip()
                    if chunk == 'data: [DONE]':
                        break
                        
                    if not chunk.startswith('data: '):
                        continue
                        
                    try:
                        data = json.loads(chunk[6:])  # Skip 'data: ' prefix
                        if not isinstance(data, dict):
                            print(f"Invalid data format: {data}")
                            continue
                            
                        choices = data.get('choices', [])
                        if not choices:
                            print("No choices in response")
                            continue
                            
                        delta = choices[0].get('delta', {})
                        if not isinstance(delta, dict):
                            print(f"Invalid delta format: {delta}")
                            continue
                            
                        content = delta.get('content', '')
                        if not content:
                            continue
                            
                        print(f"Raw chunk: {content}")
                        
                        if '<think>' in content:
                            in_think_tag = True
                            content = content.replace('<think>', '')
                            print("\nThink tag started")
                            
                        if in_think_tag:
                            if '</think>' in content:
                                in_think_tag = False
                                content = content.replace('</think>', '')
                                think_content.append(content)
                                print("\nThink tag ended")
                            else:
                                think_content.append(content)
                        else:
                            main_content.append(content)
                            print(".", end="", flush=True)
                            
                    except json.JSONDecodeError as e:
                        print(f"\nError parsing chunk: {e}")
                        continue
                        
                print("\n\n3. Response Analysis:")
                print(f"Think tag found: {len(think_content) > 0}")
                print(f"Main content length: {len(''.join(main_content))}")
                print("\nThink content:")
                print(''.join(think_content))
                print("\nMain content:")
                print(''.join(main_content))
                
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(test_api_response())
