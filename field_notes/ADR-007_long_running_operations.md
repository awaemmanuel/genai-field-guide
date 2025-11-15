# ADR-007: Handling Long-Running Operations with Resumable Agents

**Status:** Accepted  
**Date:** 2025-11-12  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, LRO, Human-in-the-loop]

## Context

Some agent tools may not return immediately. They may need to wait for external events, such as human approval or the completion of a long background task. Standard stateless agents cannot handle these scenarios, as they lose their context while waiting.

## Decision

We will use the Long-Running Operation (LRO) pattern provided by the ADK to handle tools that need to pause and resume. This involves:

1. Using the `ToolContext` parameter in tool functions to request confirmation (`tool_context.request_confirmation()`).
2. Wrapping the agent in an `App` with `ResumabilityConfig(is_resumable=True)`.
3. Implementing a workflow that detects the `adk_request_confirmation` event and resumes the agent with the approval decision, passing the `invocation_id`.

## Consequences

* **Positive:** Enables the creation of agents that can handle human-in-the-loop scenarios and other long-running tasks. Makes agents more robust and suitable for enterprise workflows.
* **Negative:** Increases the complexity of the agent and the workflow code. Requires careful state management to ensure that the agent can be resumed correctly.
