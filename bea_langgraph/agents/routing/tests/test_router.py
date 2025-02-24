"""Tests for router implementation."""

import pytest
from ..router import Router

@pytest.mark.asyncio
async def test_router_initialization():
    """Test router initialization."""
    routes = {
        "tech_support": ["error", "bug", "not working"],
        "billing": ["payment", "charge", "refund"]
    }
    router = Router(routes=routes)
    assert router.raw_routes == routes

@pytest.mark.asyncio
async def test_route_matching():
    """Test route matching logic."""
    routes = {
        "tech_support": ["error", "bug"]
    }
    router = Router(routes=routes)
    
    # Test matching route
    result = await router.route("I found a bug in the system")
    assert result == "tech_support"
    
    # Test default route
    result = await router.route("General question about service")
    assert result == "default"

@pytest.mark.asyncio
async def test_multiple_routes():
    """Test multiple route handling."""
    routes = {
        "tech_support": ["error", "bug"],
        "billing": ["payment", "charge"]
    }
    router = Router(routes=routes)
    
    # Test first route
    result = await router.route("System error occurred")
    assert result == "tech_support"
    
    # Test second route
    result = await router.route("Payment issue")
    assert result == "billing"
    
    # Test default
    result = await router.route("General inquiry")
    assert result == "default"

@pytest.mark.asyncio
async def test_case_insensitive():
    """Test case-insensitive matching."""
    routes = {
        "tech_support": ["ERROR", "Bug"]
    }
    router = Router(routes=routes)
    
    result = await router.route("error found")
    assert result == "tech_support"
    
    result = await router.route("found a BUG")
    assert result == "tech_support"
