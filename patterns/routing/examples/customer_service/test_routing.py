"""Integration tests for customer service routing example."""

import pytest
from bea_langgraph.agents.routing.router import Router
from bea_langgraph.agents.routing.models import Route

@pytest.mark.asyncio
async def test_customer_service_routing():
    """Test customer service query routing."""
    # Initialize router with customer service routes
    router = Router(
        routes=[
            Route(
                name="technical",
                description="Technical support issues",
                criteria=["error", "bug", "crash", "not working", "broken"],
                handler="technical_support_handler"
            ),
            Route(
                name="billing",
                description="Billing and refund requests",
                criteria=["refund", "charge", "payment", "bill", "subscription"],
                handler="billing_handler"
            ),
            Route(
                name="general",
                description="General product inquiries",
                criteria=["question", "help", "information", "how to"],
                handler="general_inquiry_handler"
            )
        ],
        default_handler="general_inquiry_handler"
    )
    
    # Test technical support routing
    assert await router.route("My app keeps crashing when I try to login") == "technical_support_handler"
    assert await router.route("Getting an error message during checkout") == "technical_support_handler"
    
    # Test billing routing
    assert await router.route("I need a refund for my last payment") == "billing_handler"
    assert await router.route("How do I update my subscription?") == "billing_handler"
    
    # Test general inquiry routing
    assert await router.route("How do I use this feature?") == "general_inquiry_handler"
    assert await router.route("Can you help me understand the pricing?") == "general_inquiry_handler"
    
    # Test default handler for unclassified queries
    assert await router.route("Lorem ipsum dolor sit amet") == "general_inquiry_handler"

@pytest.mark.asyncio
async def test_edge_cases():
    """Test edge cases and boundary conditions."""
    router = Router(
        routes=[
            Route(
                name="technical",
                description="Technical support issues",
                criteria=["error"],
                handler="technical_support_handler"
            )
        ],
        default_handler="general_inquiry_handler"
    )
    
    # Test empty input
    assert await router.route("") == "general_inquiry_handler"
    
    # Test case insensitivity
    assert await router.route("ERROR") == "technical_support_handler"
    assert await router.route("error") == "technical_support_handler"
    
    # Test partial matches
    assert await router.route("This has an error in it") == "technical_support_handler"
