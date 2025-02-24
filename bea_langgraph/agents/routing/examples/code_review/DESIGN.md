# Code Review Router Design

## Design Principles

Following Anthropic's guidance on building effective agents:

1. Simplicity
   - Direct keyword-based classification
   - No complex state management
   - Clear routing logic

2. Separation of Concerns
   - Router only handles classification
   - Specialists handle detailed review
   - Clear interfaces between components

3. Composability
   - Router can be used independently
   - Easy to extend with new categories
   - Simple integration with other components

## Implementation Details

### Router Configuration
```python
routes = {
    "security": ["password", "encrypt", "auth"],
    "performance": ["loop", "memory", "cpu"],
    "style": ["format", "lint", "style"],
    "testing": ["test", "assert", "mock"],
    "architecture": ["pattern", "design", "interface"]
}
```

### Design Decisions

1. Keyword-Based Routing
   - Pro: Simple and effective
   - Pro: Easy to maintain and update
   - Con: May miss context nuances
   - Mitigation: Comprehensive keyword lists

2. Default Routing
   - Pro: No code left unreviewed
   - Pro: Clear fallback behavior
   - Con: Some code may get generic review
   - Mitigation: Broad category coverage

3. Specialist Categories
   - Security: Authentication, encryption, sensitive data
   - Performance: Resource usage, optimization
   - Style: Formatting, conventions
   - Testing: Test coverage, quality
   - Architecture: Design patterns, structure
   - General: Other code aspects

## Future Considerations

1. Extensibility
   - Add new specialist categories
   - Enhance keyword lists
   - Integrate with static analysis

2. Monitoring
   - Track routing accuracy
   - Measure specialist workload
   - Identify common patterns

3. Integration
   - Connect with CI/CD
   - Add automated fixes
   - Implement feedback loops
