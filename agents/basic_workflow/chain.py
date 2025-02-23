"""
Document processing workflow implementation using LangGraph.

This module implements the Basic Workflows pattern from the Anthropic research,
providing a workflow for document generation, review, and revision.
"""

from typing import Dict, Any, List, Tuple, cast
from langgraph.graph import StateGraph, Graph
from .models import DocumentState, WorkflowConfig
from .api.client import VeniceClient

def create_generation_node(client: VeniceClient):
    """Create a node for document generation."""
    async def generate(state: Dict[str, Any]) -> Dict[str, Any]:
        doc_state = cast(DocumentState, state["document"])
        config = cast(WorkflowConfig, state["config"])
        
        messages = [
            {"role": "system", "content": "You are a document generation assistant."},
            {"role": "user", "content": f"Generate a document following these criteria: {', '.join(config.criteria)}"}
        ]
        
        content = []
        async for chunk in client.stream_completion(messages):
            if chunk.startswith("__THINK__"):
                continue
            content.append(chunk)
        
        doc_state.content = "".join(content)
        return {"document": doc_state}
    
    return generate

def create_review_node(client: VeniceClient):
    """Create a node for document review."""
    async def review(state: Dict[str, Any]) -> Dict[str, Any]:
        doc_state = cast(DocumentState, state["document"])
        config = cast(WorkflowConfig, state["config"])
        
        messages = [
            {"role": "system", "content": "You are a document review assistant."},
            {"role": "user", "content": f"""Review this document against these criteria: {', '.join(config.criteria)}
            
            Document:
            {doc_state.content}
            
            Provide specific feedback for improvement."""}
        ]
        
        feedback = []
        async for chunk in client.stream_completion(messages):
            if chunk.startswith("__THINK__"):
                continue
            feedback.append(chunk)
        
        doc_state.add_feedback("".join(feedback))
        return {"document": doc_state}
    
    return review

def create_revision_node(client: VeniceClient):
    """Create a node for document revision."""
    async def revise(state: Dict[str, Any]) -> Dict[str, Any]:
        doc_state = cast(DocumentState, state["document"])
        config = cast(WorkflowConfig, state["config"])
        
        if not doc_state.review_feedback:
            return {"document": doc_state}
        
        messages = [
            {"role": "system", "content": "You are a document revision assistant."},
            {"role": "user", "content": f"""Revise this document based on the feedback:

            Document:
            {doc_state.content}
            
            Feedback:
            {doc_state.review_feedback[-1]}
            
            Criteria:
            {', '.join(config.criteria)}"""}
        ]
        
        content = []
        async for chunk in client.stream_completion(messages):
            if chunk.startswith("__THINK__"):
                continue
            content.append(chunk)
        
        doc_state.add_revision("".join(content))
        return {"document": doc_state}
    
    return revise

class DocumentWorkflow:
    """Implementation of document processing workflow."""
    
    def __init__(self, config: WorkflowConfig, client: VeniceClient):
        """Initialize the workflow with configuration and API client."""
        self.config = config
        self.client = client
        self.graph = self._build_graph()
    
    def _build_graph(self) -> Graph:
        """Build the workflow graph with generation, review, and revision nodes."""
        # Create the graph
        graph = StateGraph()
        
        # Add nodes
        graph.add("generate", create_generation_node(self.client))
        graph.add("review", create_review_node(self.client))
        graph.add("revise", create_revision_node(self.client))
        
        # Define edges
        def should_revise(state: Dict[str, Any]) -> str:
            doc_state = cast(DocumentState, state["document"])
            config = cast(WorkflowConfig, state["config"])
            
            if not doc_state.review_feedback:
                return "review"
                
            if len(doc_state.revision_history) >= config.max_revisions:
                return "end"
                
            return "revise"
        
        # Connect nodes
        graph.add_edge("generate", "review")
        graph.add_conditional_edges("review", should_revise)
        graph.add_edge("revise", "review")
        
        # Set entry point
        graph.set_entry_point("generate")
        
        return graph.compile()
    
    async def run(self, initial_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run the workflow with optional initial state."""
        state = initial_state or {
            "document": DocumentState(content=""),
            "config": self.config
        }
        
        try:
            result = await self.graph.arun(state)
            return result
        except Exception as e:
            raise Exception(f"Workflow execution failed: {str(e)}")
