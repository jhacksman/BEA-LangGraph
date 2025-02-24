"""Tests for routing agent models."""

import pytest
from ..models import Route

def test_route_model():
    """Test Route model creation and validation."""
    route = Route(
        name="test_route",
        keywords=["test1", "test2"]
    )
    assert route.name == "test_route"
    assert len(route.keywords) == 2

def test_route_validation():
    """Test Route model validation."""
    with pytest.raises(ValueError):
        Route(name="", keywords=[])  # Empty name and keywords

    with pytest.raises(ValueError):
        Route(name="test", keywords=None)  # None keywords
