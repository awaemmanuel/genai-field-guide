# ADR-004: Task-Centric Tool Abstraction

**Status:** Accepted  
**Date:** 2025-11-11  
**Author:** Emmanuel Awa  
**Tags:** [Tooling, Design Patterns, Best Practice]

## Context

Developers often auto-generate agent tools directly from existing REST API specifications (e.g., Swagger/OpenAPI).
As highlighted in *Agent Tools & Interoperability with MCP*, this leads to:

* **Cognitive Overload:** Foundation models struggle with tools that require dozens of granular API parameters.
* **Leaky Abstractions:** The agent becomes coupled to the underlying API implementation details.
* **Misuse:** "Thin wrapper" tools often lack the business logic validation needed to prevent an agent from taking destructive actions.

## Alternatives Considered

### 1. Direct API Mapping (Status Quo)

Exposing raw API endpoints (e.g., `POST /api/v1/tickets`) directly as tools.

* *Pros:* Zero code to write (can be auto-generated).
* *Cons:* High error rate; models often hallucinate required parameters; exposes internal schema complexity to the context window.

### 2. Task-Centric Abstraction (Decision)

Creating a dedicated "Tool Layer" where each tool corresponds to a high-level user **Task**, not an API endpoint.

* *Pros:* Tools are atomic and intent-driven (e.g., `create_incident_report` vs `post_jira_ticket`); inputs can be validated *before* hitting the API; significantly reduces token usage and hallucination.
* *Cons:* Requires writing explicit wrapper code for every tool.

## Decision

We will enforce a **Task-Centric Tool Design** standard.

1. **Describe Actions, Not Implementations:** Tool names and descriptions must focus on the *business goal* (e.g., "Refund Customer") rather than the *technical method* (e.g., "Update Stripe Record").
2. **Publish Tasks, Not APIs:** Tools should encapsulate complex multi-step workflows into a single atomic action where possible.
3. **Granularity:** Tools must be as granular as possible while remaining atomic units of work.

## Consequences

* **Positive:** Agents will be more reliable and require fewer correction loops.
* **Negative:** Initial development time for tools increases as we cannot simply "dump" an SDK into the agent.
