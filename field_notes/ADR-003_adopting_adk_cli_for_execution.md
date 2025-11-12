# ADR-003: Adopting `adk run` and `adk web` for Agent Execution

**Status:** Accepted  
**Date:** 2025-11-12  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, Execution, CLI]  

## Context

The agents in this repository were initially developed with `asyncio` boilerplate code within each agent's Python file. This approach required each agent to have its own execution logic, making them more difficult to run, maintain, and test in a standardized way.

## Decision

We will adopt the `adk run` and `adk web` commands from the Agent Development Kit (ADK) CLI as the primary method for running and interacting with agents. This decision removes the need for custom `asyncio` execution logic within each agent file and provides a consistent, framework-supported approach to agent execution.

## Consequences

* **Refactoring of Agents**: All existing and future agents will be refactored to remove the `asyncio` and `if __name__ == "__main__":` blocks.
* **Standardized Execution**: Agents will now be run using `adk run <agent_path>` for individual agents or `adk web <agents_dir>` for a web-based UI for all agents in a directory.
* **`root_agent` Convention**: The main, runnable agent in each `agent.py` file must be named `root_agent` to be discoverable by the `adk` CLI.
* **Simplified Agent Code**: This change simplifies the agent code, making it more focused on the agent's logic rather than on execution boilerplate.
* **Improved Developer Experience**: The `adk` CLI provides a better developer experience for running, testing, and debugging agents.
