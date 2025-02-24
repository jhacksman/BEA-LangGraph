"""Integration tests for model selection routing example."""

import pytest
from bea_langgraph.agents.routing.router import Router
from bea_langgraph.agents.routing.models import Route

@pytest.mark.asyncio
async def test_model_selection_routing():
    """Test query routing to appropriate models."""
    # Initialize router with model selection routes
    router = Router(
        routes=[
            Route(
                name="simple",
                description="Simple or common queries",
                criteria=[
                    "what is", "how to", "where can I",
                    "help me find", "explain"
                ],
                handler="small_model_handler"
            ),
            Route(
                name="complex",
                description="Complex or unusual queries",
                criteria=[
                    "analyze", "compare", "evaluate",
                    "synthesize", "technical", "advanced"
                ],
                handler="large_model_handler"
            )
        ],
        default_handler="large_model_handler"
    )
    
    # Test simple query routing
    assert await router.route("What is the capital of France?") == "small_model_handler"
    assert await router.route("How to reset my password?") == "small_model_handler"
    assert await router.route("Help me find the nearest store") == "small_model_handler"
    
    # Test complex query routing
    assert await router.route("Analyze the implications of quantum computing") == "large_model_handler"
    assert await router.route("Compare these architectural patterns") == "large_model_handler"
    assert await router.route("Evaluate the economic impact") == "large_model_handler"
    
    # Test default handler for ambiguous queries
    assert await router.route("Something completely different") == "large_model_handler"

@pytest.mark.asyncio
async def test_model_selection_edge_cases():
    """Test edge cases for model selection routing."""
    router = Router(
        routes=[
            Route(
                name="simple",
                description="Simple queries",
                criteria=["basic"],
                handler="small_model_handler"
            )
        ],
        default_handler="large_model_handler"
    )
    
    # Test empty input
    assert await router.route("") == "large_model_handler"
    
    # Test case insensitivity
    assert await router.route("BASIC question") == "small_model_handler"
    assert await router.route("basic question") == "small_model_handler"
    
    # Test default handler for unclassified input
    assert await router.route("complex question") == "large_model_handler"
