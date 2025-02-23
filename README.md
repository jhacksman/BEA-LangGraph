# BEA-LangGraph: Building Effective Agents with LangGraph

This repository implements the agent patterns described in Anthropic's [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) research using LangGraph, a framework for building stateful multi-actor LLM applications.

## Overview

We implement each agent pattern as a standalone example, demonstrating how to build effective LLM-powered systems using composable patterns. Our implementations use venice.ai as the OpenAI-compatible API provider.

## Agent Patterns

### 1. Basic Workflows (Prompt Chaining)
Simple sequential workflows where each step's output feeds into the next step. Demonstrates:
- Task decomposition into discrete steps
- Data flow between components
- Error handling and validation
- Example: Document generation with review and revision

### 2. Routing Agents
Agents that direct requests to appropriate handlers based on content analysis. Features:
- Dynamic routing logic
- Multiple specialized handlers
- Fallback mechanisms
- Example: Customer service request router

### 3. Parallelization Patterns
Concurrent execution of multiple LLM tasks for improved throughput. Implements:
- Task batching
- Parallel processing
- Result aggregation
- Example: Bulk content analysis system

### 4. Orchestrator-Worker Pattern
Hierarchical system with a coordinator managing specialized workers. Shows:
- Task distribution
- Progress monitoring
- Resource management
- Example: Research assistant coordinating multiple analysis tasks

### 5. Evaluator-Optimizer Pattern
Self-improving system with output quality assessment. Demonstrates:
- Output evaluation criteria
- Feedback loops
- Optimization strategies
- Example: Self-improving content generator

### 6. Autonomous Agents
Long-running agents with planning and execution capabilities. Features:
- Goal-oriented planning
- Tool usage
- State management
- Example: Task automation agent

## Technical Architecture

### Backend
- LangGraph for agent orchestration
- FastAPI for API endpoints
- venice.ai for LLM API (OpenAI-compatible)
- Pydantic for data validation
- asyncio for concurrent operations

### Testing
Each pattern includes:
- Unit tests for components
- Integration tests for workflows
- Performance benchmarks
- Evaluation metrics

## Getting Started

Detailed setup and implementation guides for each pattern will be provided in their respective directories.

## Contributing

Guidelines for contributing new patterns or improvements will be added as the project evolves.

## License

[License details to be added]
