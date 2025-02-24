# Routing Pattern

## Overview
A simple workflow pattern that classifies input and directs it to specialized handlers. This pattern follows Anthropic's research on building effective agents.

## When to Use
Use this pattern when:
- You have distinct categories of tasks that are better handled separately
- Classification can be handled accurately by an LLM
- You want to optimize specialized handlers for specific types of inputs

## Examples
1. Customer Service
   - Route different types of queries (general, refund, technical) to specialized handlers
   - Each handler can be optimized for its specific task type

2. Model Selection
   - Route easy/common questions to smaller models
   - Route complex/unusual questions to more capable models

## Implementation
The routing pattern consists of three main components:
1. Router: Classifies input and selects appropriate handler
2. Routes: Defines available specialized handlers
3. Handlers: Specialized components that process specific types of input

### Key Principles
1. Keep implementation simple
   - Focus on clear input categorization
   - Avoid complex state management
   - Direct mapping to specialized handlers

2. Clear Documentation
   - Document each handler's purpose and capabilities
   - Provide examples of input types for each route

3. Separation of Concerns
   - Router only handles classification
   - Handlers focus on their specific tasks

## Design Decisions
1. Minimal State
   - Router doesn't maintain complex state
   - Focus on input classification and handler selection

2. Simple Interface
   - Clear input/output contract
   - Easy integration with other patterns

3. Error Handling
   - Default handler for unclassified inputs
   - Clear error reporting

## Integration with Model Context Protocol
The routing pattern integrates with MCP by:
1. Using standardized input/output formats
2. Supporting tool-based interactions
3. Maintaining clear documentation

## Testing
Test coverage should include:
1. Classification accuracy
2. Handler selection
3. Error cases and default handling
4. Integration with specialized handlers

## References
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
