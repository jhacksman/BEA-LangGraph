"""Tests for routing agent models."""

import pytest
from ..models import Route, RouterConfig, RoutingState

def test_route_model():
    """Test Route model creation and validation."""
    route = Route(
        name="test_route",
        description="Test route",
        criteria=["test1", "test2"],
        handler="test_handler"
    )
    assert route.name == "test_route"
    assert len(route.criteria) == 2

def test_router_config():
    """Test RouterConfig model creation and validation."""
    route = Route(
        name="test_route",
        description="Test route",
        criteria=["test1", "test2"],
        handler="test_handler"
    )
    config = RouterConfig(
        routes=[route],
        default_handler="default_handler",
        max_retries=3,
        confidence_threshold=0.7
    )
    assert len(config.routes) == 1
    assert config.default_handler == "default_handler"

def test_routing_state():
    """Test RoutingState model and methods."""
    state = RoutingState(input="test input")
    assert state.input == "test input"
    assert state.attempts == 0
    
    state.add_attempt("test_route", 0.8)
    assert state.attempts == 1
    assert len(state.history) == 1
    
    state.set_route("final_route", 0.9)
    assert state.selected_route == "final_route"
    assert state.confidence == 0.9
    assert state.attempts == 2
