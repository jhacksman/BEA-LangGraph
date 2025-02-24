"""Tests for customer service routing example."""

import pytest
from ..workflow import CustomerServiceRouter

@pytest.mark.asyncio
async def test_technical_routing():
    """Test routing of technical queries."""
    router = CustomerServiceRouter()
    
    queries = [
        "I found a bug in the application",
        "The system is not working",
        "My account is broken",
        "Login failed multiple times"
    ]
    
    for query in queries:
        result = await router.route_query(query)
        assert result in ["technical", "account"]

@pytest.mark.asyncio
async def test_billing_routing():
    """Test routing of billing queries."""
    router = CustomerServiceRouter()
    
    queries = [
        "Issue with my payment",
        "Need a refund for last charge",
        "Update billing information",
        "Cancel subscription"
    ]
    
    for query in queries:
        result = await router.route_query(query)
        assert result == "billing"

@pytest.mark.asyncio
async def test_account_routing():
    """Test routing of account queries."""
    router = CustomerServiceRouter()
    
    queries = [
        "Reset my password",
        "Can't access my account",
        "Update profile information",
        "Delete my account"
    ]
    
    for query in queries:
        result = await router.route_query(query)
        assert result == "account"

@pytest.mark.asyncio
async def test_product_routing():
    """Test routing of product queries."""
    router = CustomerServiceRouter()
    
    queries = [
        "How to use this feature",
        "Need help with setup",
        "Where is the documentation",
        "Product tutorial needed"
    ]
    
    for query in queries:
        result = await router.route_query(query)
        assert result == "product"

@pytest.mark.asyncio
async def test_general_routing():
    """Test routing of general queries."""
    router = CustomerServiceRouter()
    
    queries = [
        "General question",
        "Other inquiry",
        "Just saying hello",
        "Random feedback"
    ]
    
    for query in queries:
        result = await router.route_query(query)
        assert result == "general"
