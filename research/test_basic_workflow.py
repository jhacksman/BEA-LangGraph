"""Test script for basic workflow functionality."""

import os
import asyncio
import json
from bea_langgraph.agents.basic_workflow.api.client import VeniceClient
from bea_langgraph.agents.basic_workflow.models import DocumentState, WorkflowConfig
from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow

async def test_basic_workflow():
    """Test the basic workflow functionality."""
    print("\n=== Testing Basic Workflow ===\n")
    
    # Test document
    test_doc = """# Test Document
This is a test document for processing through our workflow.

## Key Points
1. Clear structure
2. Concise content
3. Easy to understand"""

    try:
        # Step 1: Initialize components
        print("1. Initializing components...")
        api_key = os.getenv("VENICE_API_KEY")
        if not api_key:
            raise ValueError("VENICE_API_KEY environment variable not set")
        client = VeniceClient(api_key)
        config = WorkflowConfig(
            criteria=['Clear structure', 'Concise content', 'Easy to understand'],
            max_revisions=1
        )
        workflow = DocumentWorkflow(config, client)
        print("✓ Components initialized")

        # Step 2: Test document generation
        print("\n2. Testing document generation...")
        doc_state = DocumentState(content=test_doc)
        print("Input document:", doc_state.content)
        
        # Step 3: Process document with timeout
        print("\n3. Processing document...")
        try:
            async with asyncio.timeout(60):  # Reduced timeout for testing
                # Add system message to guide response format
                messages = [
                    {"role": "system", "content": "You are a technical writer. Write clear, structured markdown documents. Keep responses under 500 characters. No analysis or explanations. Stop generating after writing a complete document."},
                    {"role": "user", "content": "Write a short project setup guide with these exact sections:\n\n# Project Setup\n\n## Prerequisites\n[List required software]\n\n## Installation\n[List installation steps]\n\n## Configuration\n[List configuration steps]"}
                ]
                result = await workflow.run({
                    'document': doc_state,
                    'config': config,
                    'messages': messages
                })
        except asyncio.TimeoutError:
            print("\n❌ Document processing timed out after 30 seconds")
            return
        except Exception as e:
            print(f"\n❌ Document processing failed: {str(e)}")
            return
        
        # Step 4: Verify results
        print("\n4. Verifying results...")
        print("\nGenerated content:")
        print(result['document'].content)
        print("\nReview feedback:")
        for i, feedback in enumerate(result['document'].review_feedback or [], 1):
            print(f"\nFeedback {i}:")
            print(feedback)
        print("\nRevision history:")
        for i, revision in enumerate(result['document'].revision_history or [], 1):
            print(f"\nRevision {i}:")
            print(revision)
            
        print("\n✓ Basic workflow test completed successfully")
        
    except Exception as e:
        print(f"\n❌ Error during workflow test: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(test_basic_workflow())
