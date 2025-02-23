"""Test script to verify document processing workflow functionality."""

from bea_langgraph.agents.basic_workflow.api.client import VeniceClient
from bea_langgraph.agents.basic_workflow.models import DocumentState, WorkflowConfig
from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow
import asyncio

import aiohttp

async def test_workflow():
    """Test the document processing workflow."""
    print("Testing API connection...")
    async with aiohttp.ClientSession() as session:
        try:
            # Test API with a simple completion request
            headers = {
                "Authorization": f"Bearer B9Y68yQgatQw8wmpmnIMYcGip1phCt-43CS0OktZU6",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-r1-671b",
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": True
            }
            async with session.post(
                "https://api.venice.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status != 200:
                    print(f"API test failed: {response.status}")
                    error_text = await response.text()
                    print(f"Error details: {error_text}")
                    return
                
                print("API connection successful, testing streaming response...")
                async for line in response.content:
                    if line:
                        chunk = line.decode('utf-8').strip()
                        if chunk and chunk != "data: [DONE]":
                            print(f"Received chunk: {chunk}")
                print("API test passed - streaming response received")
        except Exception as e:
            print(f"API connection error: {str(e)}")
            return

    content = """# Test Document

This is a test document for processing through our workflow.

## Key Points
1. Clear structure
2. Concise content
3. Easy to understand

Please review and improve this document based on the provided criteria."""

    try:
        # Test 1: API Connection
        print("\n1. Testing API Connection...")
        client = VeniceClient('B9Y68yQgatQw8wmpmnIMYcGip1phCt-43CS0OktZU6')
        print("✓ Created Venice client")
        
        # Test 2: Configuration
        print("\n2. Testing Workflow Configuration...")
        config = WorkflowConfig(
            criteria=['Clear structure', 'Concise content', 'Easy to understand'],
            max_revisions=1
        )
        print("✓ Created workflow config")
        
        # Test 3: Workflow Initialization
        print("\n3. Testing Workflow Initialization...")
        workflow = DocumentWorkflow(config, client)
        print("✓ Initialized workflow")
    
        # Test 4: Document Processing
        print("\n4. Testing Document Processing...")
        print("Starting generation phase...")
        result = await workflow.run({
            'document': DocumentState(content=content),
            'config': config
        })
        
        # Verify results
        print("\n=== Results ===")
        print("\nDocument Content:")
        print(result['document'].content)
        print("\nReview Feedback:")
        print(result['document'].review_feedback)
        print("\nRevision History:")
        print(result['document'].revision_history)
        
        print("\n✓ All tests completed successfully")
    except Exception as e:
        print(f"Error during workflow execution: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(test_workflow())
