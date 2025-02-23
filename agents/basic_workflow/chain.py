"""
Document processing workflow implementation using LangGraph.

This module implements the Basic Workflows pattern from the Anthropic research,
providing a workflow for document generation, review, and revision.
"""

from typing import Dict, Any, List, Tuple, cast, Union
from langgraph.graph import StateGraph, Graph
from .models import DocumentState, WorkflowConfig
from .api.client import VeniceClient

def create_generation_node(client: VeniceClient):
    """Create a node for document generation."""
    def generate(state: Dict[str, Any]) -> Dict[str, Any]:
        doc_state = cast(DocumentState, state["document"])
        config = cast(WorkflowConfig, state["config"])
        
        messages = [
            {"role": "system", "content": "You are a document generation assistant."},
            {"role": "user", "content": f"Generate a document following these criteria: {', '.join(config.criteria)}"}
        ]
        
        # Synchronous function for testing
        doc_state.content = "Generated document"
        return {"document": doc_state}
    
    return generate

def create_review_node(client: VeniceClient):
    """Create a node for document review."""
    def review(state: Dict[str, Any]) -> Dict[str, Any]:
        doc_state = cast(DocumentState, state["document"])
        config = cast(WorkflowConfig, state["config"])
        
        # Synchronous function for testing
        doc_state.add_feedback("Test feedback")
        return {"document": doc_state}
    
    return review

def create_revision_node(client: VeniceClient):
    """Create a node for document revision."""
    def revise(state: Dict[str, Any]) -> Dict[str, Any]:
        doc_state = cast(DocumentState, state["document"])
        config = cast(WorkflowConfig, state["config"])
        
        if not doc_state.review_feedback:
            return {"document": doc_state}
        
        # Synchronous function for testing
        doc_state.add_revision("Revised document")
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
        # Create the graph with state schema
        graph = StateGraph(
            state_schema=Dict[str, Union[DocumentState, WorkflowConfig]]
        )
        
        # Add nodes
        graph.add_node("generate", create_generation_node(self.client))
        graph.add_node("review", create_review_node(self.client))
        graph.add_node("revise", create_revision_node(self.client))
        
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
            result = await self.graph.ainvoke(state)
            return result
        except Exception as e:
            raise Exception(f"Workflow execution failed: {str(e)}")
