# ADR-008: Defaulting to Persistent Sessions for Agent State

**Status:** Accepted  
**Date:** 2025-11-14  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, State Management, Persistence]  

## Context

When building stateful agents, managing the conversation history and state is critical. The `google-adk` library provides two primary mechanisms for session management:

1. **`InMemorySessionService`**: Stores session data (events and state) in RAM. This is simple and fast for ephemeral tasks, but all history is lost when the application restarts.
2. **`DatabaseSessionService`**: Stores session data in a persistent database (e.g., SQLite), allowing conversations to be resumed across application restarts.

Our goal is to create production-grade, reusable patterns. A key characteristic of production systems is robustness and the ability to maintain state. Agents that forget their context after a restart are not suitable for most real-world use cases where users expect to continue conversations.

## Decision

We will standardize on **`DatabaseSessionService`** as the default session management mechanism for all reference implementations and architectural patterns within this repository.

`InMemorySessionService` should only be used for specific, clearly documented cases where statelessness is an explicit design choice (e.g., simple, one-shot tools that require no memory). All general-purpose and conversational agents must default to persistence.

## Consequences

* **Positive:**
  * All agent patterns will be stateful and persistent by default, reflecting a more realistic production architecture.
  * Users of the field guide will be implicitly taught to prioritize persistence in their own designs.
  * It enables the development of more advanced patterns that rely on long-term memory and context.

* **Negative:**
  * Running the agent patterns will create a local database file (e.g., `my_agent_data.db`). This requires us to update the project's `.gitignore` file to prevent these database files from being committed to the repository.
  * There is a minor performance overhead compared to the in-memory solution, though this is negligible for most use cases and a worthwhile trade-off for persistence.
