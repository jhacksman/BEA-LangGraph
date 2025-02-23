"""
Document processing workflow implementation.

This module implements the Basic Workflows pattern from the Anthropic research,
providing a workflow for document generation, review, and revision.
"""

import asyncio
from typing import Dict, Any, List, Tuple, cast, Union
from .models import DocumentState, WorkflowConfig
from .api.client import VeniceClient


class DocumentWorkflow:
    """Implementation of document processing workflow."""
    
    def __init__(self, config: WorkflowConfig, client: VeniceClient):
        """Initialize the workflow with configuration and API client."""
        self.config = config
        self.client = client
        
    async def run(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run the workflow with input state."""
        state = inputs or {
            "document": DocumentState(content=""),
            "config": self.config
        }
        
        try:
            print("\nStep 1: Document Generation")
            doc_state = cast(DocumentState, state["document"])
            messages = state.get('messages', [
                {"role": "system", "content": "You are a document generation assistant. Generate a clear, structured document based on the provided criteria."},
                {"role": "user", "content": f"Generate a document following these criteria: {', '.join(self.config.criteria)}"}
            ])
            
            # Generate initial document
            doc_state = await self._generate(doc_state, messages)
            if not doc_state.content:
                raise Exception("Document generation failed")
                
            print("\nStep 2: Document Review")
            # Review document
            feedback = await self._review(doc_state)
            if feedback:
                doc_state.add_feedback(feedback)
                
                print("\nStep 3: Document Revision")
                # Revise document based on feedback
                doc_state = await self._revise(doc_state)
            
            return {"document": doc_state, "config": self.config}
        except Exception as e:
            print(f"\nError: {str(e)}")
            raise Exception(f"Workflow execution failed: {str(e)}")
            
    async def _generate(self, doc_state: DocumentState, messages: List[Dict[str, str]] = None) -> DocumentState:
        """Generate initial document."""
        if not messages:
            messages = [
                {"role": "system", "content": "You are a document generation assistant. Generate a clear, structured document."},
                {"role": "user", "content": f"Generate a document following these criteria: {', '.join(self.config.criteria)}"}
            ]
        
        try:
            print("Generating document...")
            content_buffer = []
            try:
                async with asyncio.timeout(30):  # Timeout for generation step
                    async for chunk in self.client.stream_completion(messages, timeout=30.0):
                        if chunk.startswith("<think>"):
                            print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                            continue
                        content_buffer.append(chunk)
                        content = ''.join(content_buffer)
                        print(f"\rGenerating document... ({len(content)} chars)", end="", flush=True)
                        # Break if we have a complete document with sufficient content
                        if len(content) > 200 and content.count('\n\n') >= 2:
                            break
            except asyncio.TimeoutError:
                print("\nGeneration timed out, using partial content")
                if not content_buffer:
                    raise Exception("No content generated before timeout")
            except Exception as e:
                print(f"\nError during generation: {str(e)}")
                raise
            
            doc_state.content = "".join(content_buffer)
            print("\nDocument generation complete")
            return doc_state
        except Exception as e:
            print(f"\nError during document generation: {str(e)}")
            raise
        
    async def _review(self, doc_state: DocumentState) -> str:
        """Review document and provide feedback."""
        messages = [
            {"role": "system", "content": "You are a document review assistant."},
            {"role": "user", "content": f"Review this document against these criteria: {', '.join(self.config.criteria)}\n\nDocument:\n{doc_state.content}"}
        ]
        
        try:
            print("\nReviewing document...")
            feedback_buffer = []
            try:
                async with asyncio.timeout(30):
                    async for chunk in self.client.stream_completion(messages, timeout=30.0):
                        if chunk.startswith("<think>"):
                            print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                            continue
                        feedback_buffer.append(chunk)
                        print(".", end="", flush=True)
                        feedback = ''.join(feedback_buffer)
                        # Break if we have complete feedback
                        if len(feedback) > 200 and feedback.count('\n') >= 3:
                            break
            except Exception as e:
                print(f"\nError during review: {str(e)}")
                raise
            
            print("\nDocument review complete")
            return "".join(feedback_buffer)
        except Exception as e:
            print(f"\nError during document review: {str(e)}")
            raise
        
    async def _revise(self, doc_state: DocumentState) -> DocumentState:
        """Revise document based on feedback."""
        messages = [
            {"role": "system", "content": "You are a document revision assistant."},
            {"role": "user", "content": f"Revise this document based on the feedback:\n\nDocument:\n{doc_state.content}\n\nFeedback:\n{doc_state.review_feedback[-1]}"}
        ]
        
        try:
            print("\nRevising document...")
            revised_content = []
            try:
                async with asyncio.timeout(120):
                    async for chunk in self.client.stream_completion(messages, timeout=120.0):
                        if chunk.startswith("<think>"):
                            print(f"\nThinking: {chunk[7:-8]}")  # Strip <think> tags
                            continue
                        revised_content.append(chunk)
                        print(".", end="", flush=True)
                        content = ''.join(revised_content)
                        # Break if we have a complete revision
                        if len(content) > 200 and content.count('\n\n') >= 2:
                            break
            except Exception as e:
                print(f"\nError during revision: {str(e)}")
                raise
            
            print("\nDocument revision complete")
            doc_state.add_revision("".join(revised_content))
            return doc_state
        except Exception as e:
            print(f"\nError during document revision: {str(e)}")
            raise
