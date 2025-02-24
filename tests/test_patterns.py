"""Integration tests for all implemented patterns."""

import pytest
from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow
from bea_langgraph.agents.parallelization.workflow import ParallelWorkflow
from bea_langgraph.agents.orchestrator.workflow import OrchestratorWorkflow
from bea_langgraph.agents.evaluator.workflow import EvaluatorWorkflow
from bea_langgraph.agents.routing.examples.customer_service.workflow import CustomerServiceRouter
from bea_langgraph.agents.routing.examples.code_review.workflow import CodeReviewRouter
from bea_langgraph.agents.basic_workflow.api.client import VeniceClient
from bea_langgraph.common.mcp import MCPMessage, Tool

@pytest.mark.asyncio
async def test_pattern_integration():
    """Test integration between different patterns."""
    # Mock API client for testing
    class MockVeniceClient:
        async def stream_completion(self, messages, **kwargs):
            if "evaluate" in str(messages).lower():
                yield "Score: 0.8\nFeedback: Good clarity\nImprovements: None needed"
            else:
                yield "Test response"
    
    client = MockVeniceClient()
    
    # Test document workflow with parallelization
    doc_workflow = DocumentWorkflow(config=None, client=client)
    parallel_workflow = ParallelWorkflow(config=None, client=client)
    
    # Generate document sections in parallel
    sections = ["Section 1", "Section 2", "Section 3"]
    tasks = [
        {"task_id": f"section_{i}", "content": section}
        for i, section in enumerate(sections)
    ]
    
    parallel_result = await parallel_workflow.process_tasks(tasks)
    assert len(parallel_result.tasks) == len(sections)
    
    # Process combined document
    doc_state = await doc_workflow.run({
        "document": {"content": "\n\n".join(t.result for t in parallel_result.tasks)}
    })
    assert doc_state["document"].content
    
    # Test orchestrator with evaluator
    from bea_langgraph.agents.orchestrator.models import Task, OrchestratorConfig
    from bea_langgraph.agents.evaluator.models import EvaluatorConfig
    
    orchestrator = OrchestratorWorkflow(
        config=OrchestratorConfig(timeout_per_task=30.0),
        client=client
    )
    evaluator = EvaluatorWorkflow(
        config=EvaluatorConfig(timeout_per_evaluation=30.0),
        client=client
    )
    
    # Break down and process task
    task = Task(description="Complex task to evaluate")
    orchestrator_result = await orchestrator.execute(task)
    assert orchestrator_result.subtasks
    
    # Evaluate results
    for subtask in orchestrator_result.subtasks:
        if subtask.result:
            content, evaluation = await evaluator.evaluate_and_improve(
                subtask.result,
                criteria=["clarity", "completeness"]
            )
            assert evaluation.score >= 0.0
            assert evaluation.score <= 1.0

@pytest.mark.asyncio
async def test_routing_patterns():
    """Test routing pattern implementations."""
    # Test customer service routing
    cs_router = CustomerServiceRouter()
    
    # Technical support
    result = await cs_router.route_query("I found a bug in the system")
    assert result == "technical"
    
    # Billing support
    result = await cs_router.route_query("Issue with my payment")
    assert result == "billing"
    
    # Account support
    result = await cs_router.route_query("Can't access my account")
    assert result == "account"
    
    # Product support
    result = await cs_router.route_query("How to use this feature")
    assert result == "product"
    
    # General support
    result = await cs_router.route_query("Just saying hello")
    assert result == "general"
    
    # Test code review routing
    code_router = CodeReviewRouter()
    
    # Security review
    result = await code_router.route_review("def validate_password(password):")
    assert result == "security"
    
    # Performance review
    result = await code_router.route_review("for i in range(1000000):")
    assert result == "performance"
    
    # Style review
    result = await code_router.route_review("def badlyFormattedFunction():")
    assert result == "style"
    
    # Testing review
    result = await code_router.route_review("def test_user_login():")
    assert result == "testing"
    
    # Architecture review
    result = await code_router.route_review("class AbstractFactory:")
    assert result == "architecture"
    
    # General review
    result = await code_router.route_review("print('Hello world')")
    assert result == "general"

@pytest.mark.asyncio
async def test_mcp_integration():
    """Test MCP integration across patterns."""
    # Mock API client for testing
    class MockVeniceClient:
        async def stream_completion(self, messages, **kwargs):
            if "evaluate" in str(messages).lower():
                yield "Score: 0.8\nFeedback: Good clarity\nImprovements: None needed"
            else:
                yield "Test response"
    
    client = MockVeniceClient()
    
    # Define test tool
    tool = Tool(
        name="test_tool",
        description="Test tool",
        parameters={"param": "string"},
        examples=[{
            "input": {"param": "test"},
            "output": "success"
        }]
    )
    
    # Test with document workflow
    doc_workflow = DocumentWorkflow(config=None, client=client)
    message = MCPMessage(
        role="user",
        content="Test content",
        tools=[tool]
    )
    
    doc_state = await doc_workflow.run({
        "document": {"content": ""},
        "messages": [message.dict()]
    })
    assert doc_state["document"].content
    
    # Test with evaluator
    from bea_langgraph.agents.evaluator.models import EvaluatorConfig
    evaluator = EvaluatorWorkflow(
        config=EvaluatorConfig(timeout_per_evaluation=30.0),
        client=client
    )
    content, evaluation = await evaluator.evaluate_and_improve(
        doc_state["document"].content,
        criteria=["clarity"]
    )
    assert evaluation.score >= 0.0
    assert "think_process" in evaluation.metadata

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling across patterns."""
    # Mock API client for testing
    class MockVeniceClient:
        async def stream_completion(self, messages, **kwargs):
            if "evaluate" in str(messages).lower():
                yield "Score: 0.8\nFeedback: Good clarity\nImprovements: None needed"
            else:
                yield "Test response"
    
    client = MockVeniceClient()
    
    # Test parallel processing errors
    parallel_workflow = ParallelWorkflow(config=None, client=client)
    tasks = [
        {"task_id": "1", "content": ""},  # Empty content
        {"task_id": "2", "content": None}  # Invalid content
    ]
    
    with pytest.raises(Exception):
        await parallel_workflow.process_tasks(tasks)
    
    # Test orchestrator errors
    orchestrator = OrchestratorWorkflow(config=None, client=client)
    task = {"description": None}  # Invalid task
    
    with pytest.raises(Exception):
        await orchestrator.execute(task)
    
    # Test evaluator errors
    evaluator = EvaluatorWorkflow(config=None, client=client)
    with pytest.raises(Exception):
        await evaluator.evaluate_and_improve(None, []) # Invalid input
