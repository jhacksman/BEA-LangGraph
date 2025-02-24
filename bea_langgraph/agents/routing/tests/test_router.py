"""Tests for router implementation."""

import pytest
from ..models import Route, RouterConfig, RoutingState
from ..router import Router
from ...basic_workflow.api.client import VeniceClient

@pytest.mark.asyncio
async def test_router_initialization():
    """Test router initialization."""
    route = Route(
        name="test_route",
        description="Test route",
        criteria=["test1", "test2"],
        handler="test_handler"
    )
    config = RouterConfig(
        routes=[route],
        default_handler="default_handler"
    )
    client = VeniceClient(api_key="test_key")
    router = Router(config, client)
    assert router.config == config
    assert router.client == client

@pytest.mark.asyncio
async def test_routing_logic():
    """Test routing logic with mock API client."""
    route = Route(
        name="test_route",
        description="Test route",
        criteria=["test1", "test2"],
        handler="test_handler"
    )
    config = RouterConfig(
        routes=[route],
        default_handler="default_handler",
        confidence_threshold=0.7
    )
    client = VeniceClient(api_key="test_key")
    router = Router(config, client)
    
    state = {
        "routing": RoutingState(input="test input that matches test1 criteria")
    }
    
    try:
        result = await router.route(state)
        assert "routing" in result
        routing_state = result["routing"]
        assert routing_state.attempts >= 1
        assert routing_state.selected_route is not None
    except Exception as e:
        pytest.fail(f"Routing failed: {str(e)}")

@pytest.mark.asyncio
async def test_fallback_to_default():
    """Test fallback to default handler when confidence is low."""
    route = Route(
        name="test_route",
        description="Test route",
        criteria=["test1", "test2"],
        handler="test_handler"
    )
    config = RouterConfig(
        routes=[route],
        default_handler="default_handler",
        confidence_threshold=0.9,
        max_retries=1
    )
    client = VeniceClient(api_key="test_key")
    router = Router(config, client)
    
    state = {
        "routing": RoutingState(input="completely unrelated input")
    }
    
    try:
        result = await router.route(state)
        assert "routing" in result
        routing_state = result["routing"]
        assert routing_state.selected_route == "default_handler"
        assert routing_state.attempts > 0
    except Exception as e:
        pytest.fail(f"Fallback routing failed: {str(e)}")
