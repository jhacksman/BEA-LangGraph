# BEA-LangGraph Directory Structure

```
BEA-LangGraph/
├── agents/                      # Main agent implementations
│   ├── basic_workflow/         # Pattern 1: Basic Workflows
│   │   ├── __init__.py
│   │   ├── chain.py           # Core workflow implementation
│   │   ├── models.py          # Pydantic models
│   │   ├── prompts/           # Prompt templates
│   │   └── tests/             # Pattern-specific tests
│   │
│   ├── routing/               # Pattern 2: Routing Agents
│   │   ├── __init__.py
│   │   ├── router.py          # Router implementation
│   │   ├── handlers/          # Specialized handlers
│   │   ├── prompts/
│   │   └── tests/
│   │
│   ├── parallel/              # Pattern 3: Parallelization
│   │   ├── __init__.py
│   │   ├── executor.py        # Parallel execution logic
│   │   ├── aggregator.py      # Result aggregation
│   │   ├── prompts/
│   │   └── tests/
│   │
│   ├── orchestrator/          # Pattern 4: Orchestrator-Worker
│   │   ├── __init__.py
│   │   ├── coordinator.py     # Orchestrator implementation
│   │   ├── workers/           # Specialized workers
│   │   ├── prompts/
│   │   └── tests/
│   │
│   ├── evaluator/            # Pattern 5: Evaluator-Optimizer
│   │   ├── __init__.py
│   │   ├── evaluator.py      # Output evaluation
│   │   ├── optimizer.py      # Optimization logic
│   │   ├── prompts/
│   │   └── tests/
│   │
│   └── autonomous/           # Pattern 6: Autonomous Agents
│       ├── __init__.py
│       ├── agent.py          # Core agent implementation
│       ├── planner.py        # Planning module
│       ├── tools/            # Tool implementations
│       ├── prompts/
│       └── tests/
│
├── common/                   # Shared utilities
│   ├── __init__.py
│   ├── llm.py               # venice.ai API client
│   ├── config.py            # Configuration management
│   └── utils.py             # Shared helper functions
│
├── api/                     # FastAPI application
│   ├── __init__.py
│   ├── main.py             # FastAPI app
│   ├── routes/             # API endpoints
│   └── middleware/         # API middleware
│
├── tests/                  # Global test suite
│   ├── integration/       # Cross-pattern tests
│   └── performance/       # Benchmarks
│
├── examples/              # Usage examples
│   └── notebooks/        # Jupyter notebooks
│
├── docs/                 # Documentation
│   ├── setup.md         # Setup guide
│   └── patterns/        # Pattern-specific docs
│
├── pyproject.toml       # Project dependencies
├── README.md           # Project overview
└── .env.example       # Environment template
```

Each agent pattern directory follows a consistent structure:
- Core implementation files
- Pattern-specific prompts
- Dedicated test suite
- Example usage

The common utilities ensure consistent:
- LLM API interaction (venice.ai)
- Configuration management
- Error handling
- Logging

This structure enables:
1. Clear separation of concerns
2. Easy testing and maintenance
3. Consistent pattern implementation
4. Simple dependency management
5. Straightforward documentation
