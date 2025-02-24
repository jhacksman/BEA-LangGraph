"""Tests for code review routing example."""

import pytest
from ..workflow import CodeReviewRouter

@pytest.mark.asyncio
async def test_security_routing():
    """Test routing of security-related code."""
    router = CodeReviewRouter()
    
    code_samples = [
        "def validate_password(password: str):",
        "token = encrypt_data(user_input)",
        "auth.login(username, password)",
        "secret_key = os.getenv('API_KEY')"
    ]
    
    for code in code_samples:
        result = await router.route_review(code)
        assert result == "security"

@pytest.mark.asyncio
async def test_performance_routing():
    """Test routing of performance-related code."""
    router = CodeReviewRouter()
    
    code_samples = [
        "for i in range(1000000):",
        "cache.set(key, value)",
        "memory_usage = process.memory_info()",
        "cpu_intensive_operation()"
    ]
    
    for code in code_samples:
        result = await router.route_review(code)
        assert result == "performance"

@pytest.mark.asyncio
async def test_style_routing():
    """Test routing of style-related code."""
    router = CodeReviewRouter()
    
    code_samples = [
        "def badlyFormattedFunction():",
        "variable_name = 'not_following_convention'",
        "# TODO: fix style issues",
        "run_lint_check()"
    ]
    
    for code in code_samples:
        result = await router.route_review(code)
        assert result == "style"

@pytest.mark.asyncio
async def test_testing_routing():
    """Test routing of testing-related code."""
    router = CodeReviewRouter()
    
    code_samples = [
        "def test_user_login():",
        "mock_database = Mock()",
        "assert result == expected",
        "pytest.fixture"
    ]
    
    for code in code_samples:
        result = await router.route_review(code)
        assert result == "testing"

@pytest.mark.asyncio
async def test_architecture_routing():
    """Test routing of architecture-related code."""
    router = CodeReviewRouter()
    
    code_samples = [
        "class AbstractFactory:",
        "dependency_injection_container",
        "interface UserRepository:",
        "high_coupling_detected"
    ]
    
    for code in code_samples:
        result = await router.route_review(code)
        assert result == "architecture"

@pytest.mark.asyncio
async def test_general_routing():
    """Test routing of general code."""
    router = CodeReviewRouter()
    
    code_samples = [
        "print('Hello, world!')",
        "x = 42",
        "def simple_function():",
        "# Basic comment"
    ]
    
    for code in code_samples:
        result = await router.route_review(code)
        assert result == "general"
