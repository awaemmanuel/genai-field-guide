# ADR-017: Standardizing on runner.py for Local Testing

**Status:** Proposed
**Date:** 2025-11-19
**Author:** Emmanuel Awa
**Tags:** Testing, Convention, Developer Experience

## Context

**Problem Statement:** While `adk run` and `adk web` are the standard for running agents (per ADR-003), there is no standardized way to run a single agent for local testing and debugging directly from the source code. This makes it harder for developers to quickly test their agents without using the `adk` CLI and can lead to developers adding ad-hoc testing code to the `agent.py` file.

**Driving Factors:** The need for a consistent and convenient way to run local tests for each agent pattern. The desire to keep the `agent.py` file clean and focused on the agent definition, in line with the principle of separation of concerns.

**Assumptions:** We are developing Python-based agents and patterns.

## Alternatives Considered

### 1. No Standard for Local Testing

Leaving it up to each developer to figure out how to run local tests.

*   **Pros:** No upfront effort to define a standard.
*   **Cons:** Inconsistent testing practices, harder for new developers to get started, and can lead to clutter in the `agent.py` file.

### 2. Including Runner Logic in `agent.py`

Keeping the `if __name__ == "__main__":` block in `agent.py` for local testing.

*   **Pros:** Self-contained file.
*   **Cons:** Clutters the `agent.py` file with execution logic, which is not its primary purpose. The `agent.py` file should be a declarative definition of the agent, not a script.

### 3. Standardizing on `runner.py` (Decision)

Creating a separate `runner.py` file for each agent pattern to house the local testing logic.

*   **Pros:**
    *   **Separation of Concerns:** The `agent.py` file defines *what* the agent is, and the `runner.py` file defines *how* to run it for local testing.
    *   **Clarity:** Provides a clear and consistent way to run local tests.
    *   **Developer Experience:** Improves the developer experience by providing a simple, standardized way to test agents locally.
*   **Cons:** Adds an extra file to each pattern.

## Decision

We will standardize on creating a `runner.py` file for each agent pattern. This file will contain the necessary code to run the agent for local testing and debugging. The `runner.py` file will typically import the `root_agent` from `agent.py` and run it using an `InMemoryRunner`.

## Consequences

*   **Positive:**
    *   All patterns will have a consistent and convenient way to be run locally.
    *   The `agent.py` file will be cleaner and more focused on the agent's definition.
    *   The developer experience will be improved.

*   **Negative:**
    *   An extra file will be added to each agent pattern.

## Related Artifacts

*   `ADR-003_adopting_adk_cli_for_execution.md`
