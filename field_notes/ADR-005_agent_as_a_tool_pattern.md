# ADR-005: Agent as a Tool Pattern

**Status:** Accepted  
**Date:** 2025-11-12  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, Tooling, Design Patterns]  

## Context

Complex tasks can often be broken down into smaller, more manageable sub-tasks. Instead of creating a single, monolithic agent to handle all aspects of a complex workflow, we can create specialized agents for each sub-task. This approach promotes modularity, reusability, and maintainability.

## Decision

We will adopt the "Agent as a Tool" pattern for delegating specific tasks to specialized agents. This pattern involves a primary agent that uses one or more specialist agents as tools to perform sub-tasks. The `AgentTool` class from the Agent Development Kit (ADK) will be used to wrap a specialist agent and make it available as a tool to the primary agent.

## Consequences

* **Modularity and Reusability**: This pattern promotes the development of small, focused, and reusable agents that can be composed into more complex systems.
* **Simplified Orchestration**: The primary agent's instructions are simplified, as it only needs to know about the specialist agent's capabilities, not its internal implementation details.
* **Clear Control Flow**: The primary agent remains in control of the overall workflow. It calls the specialist agent as a tool, receives the result, and continues the conversation or workflow. This is distinct from a sub-agent pattern where control is completely handed over.
* **Improved Maintainability**: Specialist agents can be developed, tested, and maintained independently of the primary agent.
